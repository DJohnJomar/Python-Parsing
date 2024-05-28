import re

class SyntaxErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Parser:
    def __init__(self):
        self.tokenMap = self.setUpTokenMap()  
        self.result = []
        self.index = 0
        self.hasDataType = False
        self.value = 0

    def clearResult(self):
        self.result.clear()
    
    def getValue(self):
        return self.value

    def identifyNumericType(self, string):
        byte_regex = re.compile(r"-?\d+[bB]")
        short_regex = re.compile(r"-?\d+[sS]")
        long_regex = re.compile(r"-?\d+[lL]")
        float_regex = re.compile(r"-?\d+\.\d+[fF]?")
        double_regex = re.compile(r"-?\d+\.\d+([dD]|\.)?")
        int_regex = re.compile(r"-?\d+")

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
        self.skipForWhiteSpaces(input)
        if self.index < len(input) and input[self.index] == ';':
            self.checkForToken(input[self.index])
            self.index += 1
        else:
            raise SyntaxErrorException(f"Expected a semicolon at index {self.index}")

    def parseDataType(self, input: str):
        temp = ""
        self.skipForWhiteSpaces(input)
        if self.index < len(input) and input[self.index].isalpha():
            while self.index < len(input) and input[self.index].isalnum():
                temp += input[self.index]
                self.index += 1
            if temp:
                self.hasDataType = self.checkForToken(temp)
                if not self.hasDataType:
                    self.index = 0

    def parseNumber(self, input):
        temp = ""
        self.skipForWhiteSpaces(input)
        while self.index < len(input) and (input[self.index].isdigit() or input[self.index] == '.' or input[self.index] in 'fFdDlLsSbB'):
            temp += input[self.index]
            self.index += 1
        self.result.append(f"{temp} : {self.identifyNumericType(temp)}")
        self.skipForWhiteSpaces(input)
        return float(temp.rstrip('fFdDlLsSbB'))

    def parseFactor(self, input: str):
        self.skipForWhiteSpaces(input)
        if self.index < len(input) and input[self.index] == '(':
            self.checkForToken(input[self.index])
            self.index += 1
            value = self.parseExpression(input)
            self.skipForWhiteSpaces(input)
            if self.index < len(input) and input[self.index] == ')':
                self.checkForToken(input[self.index])
                self.index += 1
                self.skipForWhiteSpaces(input)
                return value
            else:
                raise SyntaxErrorException(f"Expected ')' at index {self.index}")
        elif self.index < len(input) and (input[self.index].isdigit() or input[self.index] == '.'):
            return self.parseNumber(input)
        else:
            raise SyntaxErrorException(f"Expected a digit or an expression at index {self.index}")

    def parseTerm(self, input: str):
        value = self.parseFactor(input)
        self.skipForWhiteSpaces(input)
        while self.index < len(input) and input[self.index] in '*/':
            operator = input[self.index]
            self.checkForToken(operator)
            self.index += 1
            operand = self.parseFactor(input)
            if operator == '*':
                value *= operand
            elif operator == '/':
                value /= operand
            else:
                raise SyntaxErrorException(f"Invalid operator {operator} at index {self.index}")
        self.skipForWhiteSpaces(input)
        return value

    def parseExpression(self, input: str):
        value = self.parseTerm(input)
        self.skipForWhiteSpaces(input)
        while self.index < len(input) and input[self.index] in '+-%':
            operator = input[self.index]
            self.checkForToken(operator)
            self.index += 1
            term_value = self.parseTerm(input)
            if operator == '+':
                value += term_value
            elif operator == '-':
                value -= term_value
            elif operator == '%':
                value %= term_value
            else:
                raise SyntaxErrorException(f"Invalid operator {operator} at index {self.index}")
        return value

    def parseIdentifier(self, input):
        temp = ""
        self.skipForWhiteSpaces(input)
        if self.index < len(input) and input[self.index].isalpha():
            while self.index < len(input) and (input[self.index].isalnum() or input[self.index] == '_'):
                temp += input[self.index]
                self.index += 1
            self.result.append(temp + " : Identifier")
            self.skipForWhiteSpaces(input)
        else:
            raise SyntaxErrorException(f"Expected identifier at index {self.index}")

    def parseAssignment(self, input: str):
        self.index = 0
        self.hasDataType = False
        self.value = 0
        self.parseDataType(input)
        self.parseIdentifier(input)
        if self.index < len(input) and input[self.index] == '=':
            self.checkForToken(input[self.index])
            self.index += 1
            tempValue = self.parseExpression(input)
            self.parseSemiColon(input)
        elif self.index < len(input) and self.isOperator(input[self.index]):
            temp = ""
            temp += input[self.index]
            self.index += 1
            temp += input[self.index]
            self.index += 1
            self.checkForToken(temp)
            
            self.skipForWhiteSpaces(input)
            tempValue = self.parseExpression(input)
            self.parseSemiColon(input)
        else:
            raise SyntaxErrorException(f"Expected '=' at index {self.index}")
        self.value = tempValue
