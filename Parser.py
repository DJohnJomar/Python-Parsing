import re
"""
The program follows the following BNF:
 <arithmetic expression> =:: <data type> <identifier> = <expression>;
                             |<data type> <identifier> += <expression>; // The compounds operators
                              | <identifier> += <expression>; // The compounds operators
                              | <identifier> = <expression>;
  <expression> =:: <term> {+ | - | % <term>}
  <term> =:: <factor> {* | / factor}
  <factor> =:: (<expression>) | <number> 
  <number =:: <digit> {<digit>} |  {<digit>}["."{<digit>}]
  <identifier> =:: <letter> {<letter>}
  <data type> =:: "int" |... |double
  <digit> =:: "0"| ... | "9"
  <letter> =:: "a" | ... | "Z"
"""
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

    #identifies a numercy type through regex
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

    #checks if the string exist in the maps of tokens
    def checkForToken(self, string):
        if string in self.tokenMap:
            self.result.append(f"{string} : {self.tokenMap[string]}")
            return True
        return False

    def isOperator(self, character):
        return character in {'=', '+', '-', '*', '/', '%'}

    #fills map with values
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

    #Parsing returns to zero if a data type is not present, meaning if checkForToken returns false it does not have a data type
    #Program then proceeds to parse identifier
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

    #Parses the number then returns the value
    def parseNumber(self, input):
        temp = ""
        self.skipForWhiteSpaces(input)
        while self.index < len(input) and (input[self.index].isdigit() or input[self.index] == '.' or input[self.index] in 'fFdDlLsSbB'):
            temp += input[self.index]
            self.index += 1
        self.result.append(f"{temp} : {self.identifyNumericType(temp)}")
        self.skipForWhiteSpaces(input)
        return float(temp.rstrip('fFdDlLsSbB'))

    #Parses expression within parenthesis, returns the return value of parseExpression()
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

    #Parses the terms, computes the values present in it and returns it
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

    #Parses expressions, returns the computed value
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

    #Parses identifiers
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

    #Parses the whole arithmetic expression, e.g. int x = 1+1; etc
    #Accounts for simple assignment or compound assignment (int x += value; etc)
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
