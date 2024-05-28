from Parser import Parser

class SyntaxErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Main:
    @staticmethod
    def main():
        parser = Parser()
        while True:
            try:
                input_string = input("Enter your Java Arithmetic Expression: ")
                parser.parseAssignment(input_string)
                print("\n----- Lexeme : Token Pairs -----\n")
                for token in parser.result:
                    print(token)
                print("Computed Value: "+str(parser.getValue()))
                parser.clearResult()
            except SyntaxErrorException as e:
                print(e)
                print("Invalid Input")
                parser.clearResult()
            

if __name__ == "__main__":
    Main.main()
