from Parser import Parser

class SyntaxErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Main:
  def Main():
    parser = Parser()
    while True:
        try:
            input_string = input("Enter your Java Arithmetic Expression: ")
            parser.parse_assignment(input_string)
            print("\n----- Lexeme : Token Pairs -----\n")
            for token in parser.result:
                print(token)
        except SyntaxErrorException as e:
            print(e)
            print("Invalid Input")

if __name__ == "__Main__":
    Main()