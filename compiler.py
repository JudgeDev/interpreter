""" Interpreter according to https://ruslanspivak.com/

    Current rules:
    Input - only integers
    Operations - addition
    Whitespace characters ignored
"""


# token types
# EOF indicates that there is no more input for lexical analysis
INTEGER, PLUS, MINUS, SPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'SPACE', 'EOF'


class Token:
    """ class Token

    Representation of token as type and value
    """
    def __init__(self, t_type, value):
        # token type: INTEGER, PLUS, EOF
        self.type = t_type
        # token value: 0-9, +, None
        self.value = value

    def __str__(self):
        """ String representation of the class instance

        Examples:
              Token(INTEGER, 3)
              Token(PLUS, '+')
         """
        return f'Token({self.type}, {repr(self.value)}'

    def __repr__(self):
        return self.__str__()


class Interpreter:
    """ Lexer and expression generator and evaluator """

    def __init__(self, text):
        """ Initialise parser """
        # string input e.g. "3+5"
        self.text = text
        # index to string
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception("Error parsing input")

    def get_next_token(self):
        """ Lexer / parser

        Read the next token of the input string and convert it into a token
        """

        def get_next_char(text_string):
            """ Helper function to get next character from text """

            if self.pos <= len(text_string) - 1:
                return text_string[self.pos]
            else:
                return None

        text = self.text

        current_char = get_next_char(text)

        # is index past end
        if not current_char:
            return Token(EOF, None)

        if current_char == ' ':
            token = Token(SPACE, current_char)
            self.pos += 1
            return token

        if current_char.isdigit():
            digits = ''
            while current_char.isdigit():
                digits += current_char
                self.pos += 1
                current_char = get_next_char(text)
                if not current_char:
                    break
            token = Token(INTEGER, int(digits))
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        """ Eat a token of given type

        Compare the current token type with the passed token type and if they match
        then "eat" the current token and assign the next token to the self.current_token
        otherwise raise an exception
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def eat_all(self, token_type):
        """ Eat all consecutive tokens of given type

        Compare the current token type with the passed token type and if they match
        then "eat" the current token and assign the next token to the self.current_token
        Eat all consecutive occurrences
        """
        while self.current_token.type == token_type:
            self.current_token = self.get_next_token()

    def expr(self):
        """ Convert string into expression, verify the sequence of tokens and calculate result

        Get each token
        Use the helper method eat to verify that the token type matches the current token type
        Generate the result by adding the value of the token on the left side of the PLUS and
        the right side of the PLUS
        ?? Could modify eat to only check and let expr get the next token and throw the error ??
        If the structure in the stream of tokens does not correspond to the expected one
        e.g. INTEGER PLUS INTEGER sequence of tokens the eat method throws an exception
        """

        # first token of string
        self.current_token = self.get_next_token()

        # first non-space token should be integer
        self.eat_all(SPACE)
        left = self.current_token
        self.eat(INTEGER)

        # next non-space token should be a '+' or '-'
        self.eat_all(SPACE)
        op = self.current_token
        if self.current_token.type == PLUS:
            self.eat(PLUS)
        if self.current_token.type == MINUS:
            self.eat(MINUS)

        # next non-space is integer
        self.eat_all(SPACE)
        right = self.current_token
        self.eat(INTEGER)

        # current token should now be eof

        # now method has found sequence of tokens INTEGER PLUS INTEGER

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value + right.value

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(f"{text} = {result}")


if __name__ == '__main__':
    main()
