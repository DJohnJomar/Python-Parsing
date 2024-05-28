import re


class Parser:

    def __init__(self):
        pass

    def identifyNumericType(self, string):
        # Regular expressions to match different numeric types
        byte_regex = r"-?\d+[bB]"
        short_regex = r"-?\d+[sS]"
        int_regex = r"-?\d+"
        long_regex = r"-?\d+[lL]"
        float_regex = r"-?\d+\.\d+[fF]?"
        double_regex = r"-?\d+\.\d+([dD]|\.)?"

        # Checking if the input string matches one of the patterns
        if re.fullmatch(byte_regex, string):
            return "Byte Literal"
        elif re.fullmatch(short_regex, string):
            return "Short Literal"
        elif re.fullmatch(int_regex, string):
            return "Integer Literal"
        elif re.fullmatch(long_regex, string):
            return "Long Literal"
        elif re.fullmatch(float_regex, string):
            return "Float Literal"
        elif re.fullmatch(double_regex, string):
            return "Double Literal"
        else:
            return "Not a numeric type"

    def check_for_token(self, string, token_map):
        if string in token_map:
            return f"{string} : {token_map[string]}"
            return None

    def isOperator(self, character):
        return character in {'=', '+', '-', '*', '/', '%'}