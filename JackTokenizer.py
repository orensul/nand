"""
* Removes all comments and white space from the input stream and breaks
it into Jack language tokens, as specified by the Jack grammar.
"""

class JackTokenizer:
        def __init__(self):
            """
            Constructor
            """

        def has_more_tokens(self):
            """
            Do we have more tokens in the input?
            :return: boolean - yes - we have more tokens, no - we dont have
            """

        def advance(self):
            """
            Gets the next token from the input and makes it the current token.
            This method should only be called if hasMoreTokens() is true.
            Initially there is no current token.
            """

        def token_type(self):
            """
            :return: the type of the current token.
            """

        def key_word(self):
            """
            :return: the keyword which is the current token.
            Should be called only when tokenType() is KEYWORD.
            """

        def symbol(self):
            """
            :return: the character which is the current token.
            Should be called only when tokenType() is SYMBOL.
            """
        def identifier(self):
            """
            :return: the identifier which is the current token.
            Should be called only when tokenType() is IDENTIFIER
            """

        def int_val(self):
            """
            :return: the integer value of the current token.
            Should be called only when tokenType() is INT_CONST
            """

        def string_val(self):
            """

            :return: the string value of the current token, without the double quotes.
            Should be called only when tokenType() is STRING_CONST.
            """



