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
START_PARENTHESES = '('
END_PARENTHESES = ')'
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

# "[^"]*" - any line with " some code "
# [^"] that's mean negated set - match any character that is not "
string_pattern = r'("[^"]*")'
# | to match one of the keywords from dictionary
keywords_pattern = '(' + r'|'.join(keywords) + ')' + r'\b'
# d+ - one or more digits
numeric_pattern = r'(\d+)'
# [\w]+ - match any word character which appear one or more times
identifier_pattern = r'([\w]+)'
# first, concat all of the symbols from symbols dictionary with "\" = escape character
# to do so we can't add  by + "\" so we must use re.escape()
concat_symbols_dict_escape_char = re.escape(''.join(symbols))
# [] that's mean match one of the symbols inside
symbols_pattern = r'([' + concat_symbols_dict_escape_char + '])'


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
            self.file_as_string_without_comments = self.remove_comments\
                (self.file_as_string)
            self.token_regex = self.create_token_regex()
            self.create_list_of_tokens(self.file_as_string_without_comments)

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

        def create_token_regex(self):
            """
            :param str: the string of the (original) text in the file
            :return: token_regex - a regex which capture a token in the string
            """
            token_pattern =  keywords_pattern+'|'+symbols_pattern+'|'+numeric_pattern+ \
                             '|'+string_pattern+"|"+identifier_pattern
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

        def remove_comments(self, str):
            """
            This methods gets str which is the text of the jack file in a string, and
            removes all of the comments from it, actually crates str_without_comments
            which is a new string without the comments.
            :param str: string which is the text of the jack file
            :return: new string without comments
            """
            str_without_comments = ''
            str_list = list(str)
            idx = 0
            while idx < len(str_list) - 1:
                # if we are in a string
                if str_list[idx] == ACRONYM:
                    str_without_comments += str_list[idx]
                    idx += 1
                    # advance till end of string
                    while not str_list[idx] == ACRONYM:
                        str_without_comments += str_list[idx]
                        idx += 1
                    str_without_comments += str_list[idx]
                    idx += 1
                # if we start a multi line block comment /*
                elif str_list[idx]+str_list[idx+1] == MULTI_LINE_START_COMMENT:
                    idx += 2
                    if str_list[idx]+str_list[idx+1] == MULTI_LINE_END_COMMENT:
                        str_without_comments += ' '
                    # advance till end of multi line block comment
                    while not str_list[idx] + str_list[idx+1] == MULTI_LINE_END_COMMENT:
                        idx += 1
                    idx += 2
                    str_without_comments += ' '
                # if we start a line comment
                elif str_list[idx]+str_list[idx+1] == LINE_COMMENT:
                    idx += 2
                    # advance till end of line
                    while not str_list[idx] == LINE:
                        idx += 1
                    idx += 1
                    str_without_comments += ' '
                # otherwise, advance
                else:
                    str_without_comments += str_list[idx]
                    idx += 1

            return str_without_comments

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







