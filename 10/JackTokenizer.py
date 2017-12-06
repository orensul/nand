import re

# constants
SEMICOLON = ';'
COMMA = ','
DOT = '.'
START_CURVE_PARENTHESES = '{'
END_CURVE_PARENTHESES = '}'
LINE_COMMENT = '//'
MULTI_LINE_START_COMMENT = '/*'
MULTI_LINE_END_COMMENT = '*/'
LINE = '\n'
ACRONYM = '"'
START_PARENTHESES = "("
END_PARENTHESES = ")"
START_BRACKETS = '['
END_BRACKETS = ']'
KEYWORD = 0
SYMBOL = 1
INT_CONST = 2
STRING_CONST = 3
IDENTIFIER = 4

START_POS = 0
END_POS = 1

symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|',
           '<', '>', '=', '~']
keywords = ["class", 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
            'let', 'do',  'if', 'else', 'while', 'return']
tokens = ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier']
keyword_constant = ['true', 'false', 'null', 'this']

# regex patterns

# comment can be // (single line comment) or /* some code */ (multi line comment)
# therefore we have | and () for each group = each type of comment
# //.* that's mean a line which starts with // and then every character except line break
# zero or more times. ?$ that's mean match the end of line if multi_line flag is on
# and we will turn it on in the regex matcher.
# or /\*(.*?)\*/ that's mean code which starts in \* and end with */ and in the middle
# .*? any character zero or more times.
comment_pattern = r'(' + LINE_COMMENT + '.*?$)|(/\*(.*?)\*/)'
# "[^"]*" - any line with " some code "
# [^"] that's mean negated set - match any character that is not "
string_pattern = r'"[^"]*"'
# | to match one of the keywords from dictionary
keywords_pattern = r'|'.join(keywords)
# d+ - one or more digits
numeric_pattern = r'\d+'
# [\w]+ - match any word character which appear one or more times
identifier_pattern = r'[\w]+'
# first, concat all of the symbols from symbols dictionary with "\" = escape character
# to do so we can't add  by + "\" so we must use re.escape()
concat_symbols_dict_escape_char = re.escape(''.join(symbols))
# [] that's mean match one of the symbols inside
symbols_pattern = r'[' + concat_symbols_dict_escape_char + ']'


class JackTokenizer:
        """
        Removes all comments and white space from the input stream and breaks
        it into Jack language tokens, as specified by the Jack grammar.
        """

        def __init__(self, folder_path, jack_file_name):
            """
            Constructor
            """
            self.string_indices = []
            self.comment_indices = []
            self.tokens = []
            self.tokens_counter = 0
            self.jack_file_path = folder_path + jack_file_name
            self.jack_lines = []
            self.file_as_string = self.read_file(self.jack_file_path)
            self.token_regex = self.create_token_regex(self.file_as_string)

            # create string of the text file without the comments
            file_as_string_without_comments = ''
            for start_end_pos in self.pos_exclude_comments(len(self.file_as_string)):
                file_as_string_without_comments += \
                    self.file_as_string[start_end_pos[START_POS]:start_end_pos[END_POS]]
            # populate the output_list with the tokens
            self.create_list_of_tokens(file_as_string_without_comments)

        def advance(self):
            """
            Set the current token and increase tokens_counter by one, so next time
            this method will give us the next token in the list.
            :return: current token from list
            """
            curr_token = self.tokens[self.tokens_counter]
            self.tokens_counter += 1
            return curr_token

        def peek_next_token(self):
            """
            Only peek to the next token, without increase the counter
            :return: curren token from list
            """
            return self.tokens[self.tokens_counter]

        def is_comment_in_range_of_string(self, start_comment_pos):
            """
            :param start_comment_pos:
            :return True if the comment inside string, Otherwise, false.
            """
            for start_end_pos in self.string_indices:
                # if start of comment inside string
                if start_end_pos[START_POS] < start_comment_pos and start_comment_pos < \
                        start_end_pos[END_POS]:
                    return True
            return False

        def pos_exclude_comments(self, str_length):
            """
            This method makes us a list of all of the positions of chars in the file
            which are not inside a comment.
            :param str_length: the length of the string of the content of the file
            """
            output_list = []
            end_pos = self.comment_indices[0][1]

            for start_end_pos in self.comment_indices:
                start_pos = start_end_pos[START_POS]
                # append to output list all the numbers between tuples
                if start_pos > end_pos + 1:
                    output_list.append((end_pos + 1, start_pos - 1))
                end_pos = start_end_pos[END_POS]
                # if comment inside string we want to add the position of start, end
                # of the comment because it's not actually a "real" comment
                if self.is_comment_in_range_of_string(start_pos):
                    output_list.append((start_pos - 1, end_pos + 1))
            # add positions from the end of the last tuple to the length of the string
            # which is the max position in the file
            if str_length > end_pos + 1:
                output_list.append((end_pos + 1, str_length))
            # also, from the beginning
            if self.comment_indices[0][0] > 0:
                output_list = [(0, self.comment_indices[0][0] - 1)] + output_list
            return output_list

        def create_token_regex(self, str):
            """
            :param str: the string of the (original) text in the file
            :return: token_regex - a regex which capture a token in the string
            """
            # MULTILINE- Matches the start of the string, and in MULTILINE mode also
            # matches immediately after each newline.
            # DOTALL- matches any character including a newline.

            comment_regex = re.compile(comment_pattern, re.MULTILINE | re.DOTALL)
            string_regex = re.compile(string_pattern, re.MULTILINE | re.DOTALL)
            # extract the start position and end position in the file of strings
            self.string_indices = [m.span() for m in re.finditer(string_regex,
                                                                 str)]
            # extract the start position and end position in the file of comments
            self.comment_indices = [m.span() for m in re.finditer(comment_regex,
                                                                  str)]

            # token_pattern is or on all of the patterns, so we create token if one of
            # the pattern is captured, we add () to differentiate the groups for each
            # optional pattern
            token_pattern = START_PARENTHESES + keywords_pattern + END_PARENTHESES + "|"\
                           + START_PARENTHESES + symbols_pattern + END_PARENTHESES + "|"\
                           + START_PARENTHESES + numeric_pattern + END_PARENTHESES + "|"\
                           + START_PARENTHESES + string_pattern +  END_PARENTHESES + "|"\
                           + START_PARENTHESES + identifier_pattern + END_PARENTHESES
            return re.compile(token_pattern, re.MULTILINE | re.DOTALL)

        def create_list_of_tokens(self, string_without_comments):
            """
            This method create the list of tokens.
            :param string_without_comments: the text of the file after comments has
            been removed
            """
            for item in self.token_regex.findall(string_without_comments):
                if item[KEYWORD] != '':
                    self.tokens.append((item[KEYWORD], tokens[KEYWORD]))
                elif item[SYMBOL] != '':
                    self.tokens.append((item[SYMBOL], tokens[SYMBOL]))
                elif item[INT_CONST] != '':
                    self.tokens.append((item[INT_CONST], tokens[INT_CONST]))
                elif item[STRING_CONST] != '':
                    string = item[STRING_CONST][1:-1]
                    self.tokens.append((string, tokens[STRING_CONST]))
                elif item[IDENTIFIER] != '':
                    self.tokens.append((item[IDENTIFIER], tokens[IDENTIFIER]))

        def read_file(self, jack_file):
            """
            This method opens the jack_file which is the input and extracts his data into
            jack_lines list
            :param jack_file: the path of the jack_file
            """
            file_as_string = ""
            # open the input jack file for reading
            file = open(jack_file, 'r').read().splitlines()

            for line in file:
                file_as_string += line.strip()
                file_as_string += "\n"

            return file_as_string







