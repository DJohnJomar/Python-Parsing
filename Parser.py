import re


class Parser:

    #global Variables
    tokenMap = {}
    result = []
    index = 0
    input = None
    hasDataType = False

    def __init__(self):
        tokenMap = setUpTokenMap()

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

    def checkForToken(self, string, token_map):
        if string in token_map:
            return f"{string} : {token_map[string]}"

    def isOperator(self, character):
        return character in {'=', '+', '-', '*', '/', '%'}

    
    def setUpTokenMap(self):
        token_map = {
        "byte": "Keyword",
        "short": "Keyword",
        "int": "Keyword",
        "long": "Keyword",
        "float": "Keyword",
        "double": "Keyword",
        "=": "Equal Sign",
        "+": "Plus Sign",
        "-": "Minus Sign",
        "*": "Multiplication Sign",
        "/": "Division Sign",
        "%": "Modulo Sign",
        "++": "Increment sign",
        "--": "Decrement Sign",
        "+=": "Compound Addition",
        "-=": "Compound Subtractions",
        "*=": "Compound Multiplication",
        "/=": "Compound Division",
        "%=": "Compound Modulo",
        "(": "Open Parenthesis",
        ")": "Close Parenthesis",
        ";": "Semicolon"
        }
        return token_map
    
    def skipForWhiteSpaces(self, input):
        while index < len(input) and input[index] == ' ':
            index += 1

    def parseDataType(self, input:str):
        pass
    def parseIdentifier(self, input:str):
        pass

    def parseAssignment(self, input:str):
        temp = ""
        parseDataType(input)
        parseidentifier(input)

        if index < len(input) and input[index] == '=':
            temp += input[index]
            checkForToken(temp)
            index++
            



    

   