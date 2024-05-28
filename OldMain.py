import re

def identify_numeric_type(string):
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

def check_for_token(string, token_map):
    if string in token_map:
        return f"{string} : {token_map[string]}"
    return None

def is_operator(character):
    return character in {'=', '+', '-', '*', '/', '%'}

def parse_assignment(input_string, token_map):
    result = []
    index = 0
    input_length = len(input_string)

    def skip_for_white_spaces():
        nonlocal index
        while index < input_length and input_string[index] == ' ':
            index += 1

    def parse_data_type():
        nonlocal index
        temp = ''
        skip_for_white_spaces()
        while index < input_length and input_string[index].isalpha() and input_string[index] != '=':
            temp += input_string[index]
            index += 1
        if temp:
            return temp
        return None

    def parse_identifier():
        nonlocal index
        temp = ''
        skip_for_white_spaces()
        if index < input_length and input_string[index].isalpha():
            while index < input_length and (input_string[index].isalnum() or input_string[index] == '_'):
                temp += input_string[index]
                index += 1
            if temp:
                return temp
        return None

    def parse_number():
        nonlocal index
        temp = ''
        skip_for_white_spaces()
        while index < input_length and (input_string[index].isdigit() or input_string[index] == '.'):
            temp += input_string[index]
            index += 1
        if temp:
            return temp
        return None

    def parse_expression():
        nonlocal index
        parse_term()
        while index < input_length and input_string[index] in {'+', '-', '%'}:
            result.append(check_for_token(input_string[index], token_map))
            index += 1
            parse_term()

    def parse_term():
        nonlocal index
        parse_factor()
        while index < input_length and input_string[index] in {'*', '/'}:
            result.append(check_for_token(input_string[index], token_map))
            index += 1
            parse_factor()

    def parse_factor():
        nonlocal index
        skip_for_white_spaces()

        if index < input_length and input_string[index] == '(':
            index += 1
            parse_expression()
            if index < input_length and input_string[index] == ')':
                index += 1
        elif input_string[index].isdigit():
            num = parse_number()
            if num:
                result.append(f"{num} : {identify_numeric_type(num)}")
        elif input_string[index].isalpha():
            identifier = parse_identifier()
            if identifier:
                result.append(f"{identifier} : Identifier")
        elif input_string[index] in {'+', '-'}:
            op = input_string[index]
            if index + 1 < input_length and input_string[index + 1] == op:
                result.append(check_for_token(op * 2, token_map))
                index += 2

    data_type = parse_data_type()
    if data_type:
        result.append(check_for_token(data_type, token_map))
    else:
        raise SyntaxErrorException("Expected data type keyword")

    identifier = parse_identifier()
    if identifier:
        result.append(f"{identifier} : Identifier")
    else:
        raise SyntaxErrorException("Expected identifier")

    skip_for_white_spaces()
    if index < input_length and input_string[index] == '=':
        result.append(check_for_token('=', token_map))
        index += 1
        parse_expression()
    elif index < input_length and input_string[index] in {'+', '-', '*', '/'}:
        op = input_string[index]
        if index + 1 < input_length and input_string[index + 1] == '=':
            result.append(check_for_token(f"{op}=", token_map))
            index += 2
            parse_expression()
    else:
        raise SyntaxErrorException("Expected '=' or compound operator")

    skip_for_white_spaces()
    if index < input_length and input_string[index] == ';':
        result.append(check_for_token(';', token_map))
        index += 1
    else:
        raise SyntaxErrorException("Expected semicolon")

    return result

class SyntaxErrorException(Exception):
    pass

def setup_token_map():
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

def main():
    token_map = setup_token_map()
    print("Sample Inputs: \n\tx = x+5; \n\tint nummber = number*(5+x/3-1+7)/43*5;")
    while True:
        try:
            input_string = input("\nEnter your Java Arithmetic Expression: ")
            result = parse_assignment(input_string, token_map)
            print("\n----- Lexeme : Token Pairs -----\n")
            for token in result:
                print(token)
        except SyntaxErrorException as e:
            print(e)
            print("Invalid Input")

if __name__ == "__main__":
    main()
