import re

class SyntaxErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Parser:
    # Instance Variables
    tokenMap = {}
    result = []
    index = 0
    input = None
    hasDataType = False

    def __init__(self):
        self.tokenMap = self.setUpTokenMap()  # Correctly initialize the tokenMap instance variable

    def clearResult(self):
        self.result.clear()

    def identifyNumericType(self, string):
        # Compiled regular expressions to match different numeric types
        byte_regex = re.compile(r"-?\d+[bB]")
        short_regex = re.compile(r"-?\d+[sS]")
        long_regex = re.compile(r"-?\d+[lL]")
        float_regex = re.compile(r"-?\d+\.\d+[fF]?")
        double_regex = re.compile(r"-?\d+\.\d+([dD]|\.)?")
        int_regex = re.compile(r"-?\d+")

        # Checking if the input string matches one of the patterns
        if byte_regex.fullmatch(string):
            return "Byte Literal"
        elif short_regex.fullmatch(string):
            return "Short Literal"
        elif long_regex.fullmatch(string):
            return "Long Literal"
        elif float_regex.fullmatch(string):
            return "Float Literal"
        elif double_regex.fullmatch(string):
            return "Double Literal"
        elif int_regex.fullmatch(string):
            return "Integer Literal"
        else:
            return "Not a numeric type"

    def checkForToken(self, string):
        if string in self.tokenMap:
            self.result.append(f"{string} : {self.tokenMap[string]}")
            return True
        return False

    def isOperator(self, character):
        return character in {'=', '+', '-', '*', '/', '%'}

    def setUpTokenMap(self):
        tokenMap = {
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
            "-=": "Compound Subtraction",
            "*=": "Compound Multiplication",
            "/=": "Compound Division",
            "%=": "Compound Modulo",
            "(": "Open Parenthesis",
            ")": "Close Parenthesis",
            ";": "Semicolon"
        }
        return tokenMap
    
    def skipForWhiteSpaces(self, input):
        while self.index < len(input) and input[self.index] == ' ':
            self.index += 1

    def parseSemiColon(self, input):
        temp = ""
        self.skipForWhiteSpaces(input)

        if self.index < len(input) and input[self.index] == ';':
            temp += input[self.index]
            self.index += 1
            self.checkForToken(temp)
        else:
            raise SyntaxErrorException(f"Expected a semicolon at index {self.index}")


    

    def parseDataType(self, input: str):
        temp = ""
        self.skipForWhiteSpaces(input)

        if self.index < len(input) and input[self.index].isalpha():
            while self.index < len(input) and input[self.index].isalnum() and input[self.index] != '=':
                temp += input[self.index]
                self.index += 1
            
            if temp:
                self.hasDataType = self.checkForToken(temp)
                if not self.hasDataType:
                    self.index = 0



    def parseNumber(self, input):
        temp = ""
        self.skipForWhiteSpaces(input)

        while self.index < len(input) and input[self.index].isdigit() or input[self.index] == '.':
            temp += input[self.index]
            self.index += 1
        self.result.append(f"{temp} : {self.identifyNumericType(temp)}")
        self.skipForWhiteSpaces(input)


    def parseFactor(self, input:str):
        temp = ""
        self.skipForWhiteSpaces(input)

        if self.index < len(input) and input[self.index] == '(':
            temp += input[self.index]
            self.checkForToken(temp)
            self.index += 1
            self.parseExpression(input)
            self.skipForWhiteSpaces(input)
            if self.index < len(input) and input[self.index] == ')':
                temp = ")"
                self.checkForToken(temp)
                self.index += 1
                self.skipForWhiteSpaces(input)
            else:
                raise SyntaxErrorException(f"Expected ')' at index {self.index}")
            
        elif input[self.index].isdigit():
            self.parseNumber(input)
        
        else:
            raise SyntaxErrorException(f"Expected a digit or an expression at index {self.index}")

    def parseTerm(self, input:str):
        temp = ""
        self.skipForWhiteSpaces(input)
        self.parseFactor(input)

        while self.index < len(input) and input[self.index] in '*/':
            temp += input[self.index]
            self.checkForToken(temp)
            self.index += 1
            temp = ""
            self.parseFactor(input)
        self.skipForWhiteSpaces(input)

    def parseExpression(self, input:str):
        temp = ""
        self.skipForWhiteSpaces(input)
        self.parseTerm(input)

        while self.index < len(input) and input[self.index] in '+-%':
            temp += input[self.index]
            self.checkForToken(temp)
            self.index += 1
            temp = ""
            self.parseTerm(input)
        
        self.skipForWhiteSpaces(input)

    def parseIdentifier(self, input):
        temp = ""
        self.skipForWhiteSpaces(input)

        if self.index < len(input) and input[self.index].isalpha():
            while self.index < len(input) and input[self.index].isalnum() or input[self.index] == '_':
                temp += input[self.index]
                self.index += 1
            self.result.append(temp + " : Identifier")
            self.skipForWhiteSpaces(input)
        else:
            raise SyntaxErrorException(f"Expected identifier at index {self.index}")


    def parseAssignment(self, input: str):
        self.index = 0
        self.hasDataType = False
        temp = ""
        self.parseDataType(input)
        self.parseIdentifier(input)

        if self.index < len(input) and input[self.index] == '=':
            temp += input[self.index]
            self.checkForToken(temp)
            self.index += 1  # Correct increment syntax
            self.parseExpression(input)
            self.parseSemiColon(input)

        elif self.index < len(input) and self.isOperator(input[self.index]):
            temp += input[self.index]
            index += 1
            temp += input[self.index]
            self.checkForToken(temp)
            index += 1

            self.parseExpression(input)
            self.parseSemiColon(input)
        else:
            raise SyntaxErrorException(f"Expected '=' at index {self.index}")




