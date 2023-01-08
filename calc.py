from typing import Tuple, List
from sys import stderr

vars = dict()

# TODO: Implement negative numbers
# TODO: Implement decimal numbers


# Helper Functions

def guess_statement_type(user_input: str) -> str:
    return "assignment" if "=" in user_input else "expression"


def is_var_or_alnum(s: str) -> bool:
    for i in s:
        if (i.isalnum() or i == "$") == False:
            return False

    return True


def take_input():
    user_input = input(">>> ")
    return user_input


def get_highest_operator_index(expression: List[str]) -> int:
    # Returns -1 if no operator found
    op_dic = {"/": 0, "*": 1, "+": 2, "-": 3}
    ops = {"/", "*", "+", "-"}

    curr_op, curr_op_index = None, None

    for index, item in enumerate(expression):
        if item not in ops:
            continue

        if curr_op == None or op_dic[item] < op_dic[curr_op]:
            curr_op = item
            curr_op_index = index

    return (curr_op, curr_op_index) if curr_op_index != None else (None, -1)


def calculate(operator: str, arg1: float, arg2: float):

    if operator == "/":
        return arg1 / arg2

    elif operator == "*":
        return arg1 * arg2

    elif operator == "+":
        return arg1 + arg2

    elif operator == "-":
        return arg1 - arg2

    raise ValueError(f"Expecter operator to be one of / * + - but instead got '{operator}'")


def replace_array_values_with_value(array: List, start_index: int, end_index: int, value: any):
    for _ in range(end_index - start_index + 1):
        array.pop(start_index)

    array.insert(start_index, value)
    print(array)

    return array


def get_ending_bracket_index(iterable, br_index: int) -> int | None:
    if iterable[br_index] != "(":
        raise ValueError(f"Invalid br_index value! The character is '{iterable[br_index]}' but expected '('")

    bracket_num = 0

    for index, value in enumerate(iterable[br_index:]):
        if value == "(":
            bracket_num += 1
        elif value == ")":
            bracket_num -= 1
        else:
            continue
        if bracket_num == 0:
            return index + br_index

    return None


def replace_vars(words: List[str]) -> List[str]:
    global vars
    for index, value in enumerate(words):
        if "$" in value:
            var_name = words[index][words[index].index("$"):]
            # Replacing with 1 will be the default behaviour for undefined vars
            words[index] = words[index].replace(var_name, str(vars.get(value, "1")))

    return words


# Functions for validating and processing user input

def validate_assignment(user_input: str) -> Tuple[bool, List[str]]:
    # This method validates the given user input.
    # It assumes that the user input is an assignment statement

    eq_num = user_input.count("=")

    if eq_num > 1:
        return False, "More than one '=' in the assignment statement!"
    elif eq_num < 1:
        raise ValueError("Expected '=' in the statement!")

    if user_input.strip()[0] == "=":  # There is no variable. It starts with an '='
        return False, "There is no left side of this assignment statement!"

    if user_input.strip()[-1] == "=":  # There is no calculation. It ends with an '='
        return False, "There is no right side of this assignment statement!"

    var_side, calc_side = user_input.strip().split("=")

    var_side = var_side.strip()
    calc_side = calc_side.strip()

    # Make sure the var_side is valid
    if " " in var_side:
        return False, "The left side of the assignment statement is messed up! It has an unexpected space which should have been stripped out!"  # TODO: Change the error message

    if var_side[0] != "$":
        return False, "Expected an variable identifier on the left side but found none!"

    for char in var_side[1:]:
        if char.isalnum() == False:
            return False, "Invalid character {char} on the left side of the equation!"

    return True, [var_side, calc_side]


def validate_calculation(user_input: str) -> Tuple[bool, List[str] | str]:
    # This method validates the given user input.
    # It assumes that the user input is an expression that is to be evaulated and NOT an assignment statement

    bracket_num = 0
    started_var = False
    saw_operator = False
    words: List[str] = []  # This is supposed to look something like this ["$asdf", "*", "(", "2", "+", "4", ")"]
    curr_word = ""

    def append_curr_word():
        nonlocal curr_word
        if curr_word != "":
            words.append(curr_word)
            curr_word = ""

    for index, char in enumerate(user_input):
        if char == " ":
            continue

        # If the variable indicator '$' has been typed and the next character is not alphanumeric
        if started_var == True and char.isalnum() == False:
            # If $ was the only character typed, we expected another character
            if len(curr_word) == 1:
                return False, f"Unexpected character '{char}' at index {index}. Expected alphanumeric character after '$'."
            # If there were other characters typed, that means the variable call has ended
            else:
                started_var = False

        if (started_var == False and char.isnumeric() == False) or (started_var == True and char.isalnum() == False):
            append_curr_word()

        if char in ["$", "("] and saw_operator == False and len(words) != 0 and words[-1] != "(":
            words.append("*")

        if char.isalnum():
            saw_operator = False
            if started_var == False and char.isnumeric() == False:
                return False, f"Unexpected character '{char}' at index {index}. If you wanted to use a variable, please remember to use the '$' at the start."
            curr_word += char

        elif char in ["+", "*", "-", "/"]:
            # If we have already seen an operator
            if saw_operator == True:
                return False, f"Unexpected operator '{char}' at index {index}!"

            # If there is not a number or variable before operator
            # TODO: Figure out how to fix cases like 2(-2). How to change the polarity of the next number
            # Currently we could just append the operator to curr_word if it is either - or +. But we need to make sure that the next thing is a number or a variable
            if len(words) == 0 or is_var_or_alnum(words[-1]) == False:  # TODO: Fix the edge case of $asdf
                return False, f"Expected something before operator at index {index}"

            saw_operator = True
            words.append(char)

        elif char in ["(", ")"]:
            bracket_num = bracket_num + (1 if char == "(" else -1)

            words.append(char)

            if bracket_num < 0:
                return False, f"Unexpected character ')' at index {index}!"

        elif char == "$":
            started_var = True
            curr_word += char
        else:
            return False, f"Unexpected character '{char}' at index {index}!"

        # If the character we saw was not an operator, update the variables
        if char not in ["+", "*", "-", "/"]:
            saw_operator = False

    if curr_word != "":
        words.append(curr_word)

    if bracket_num != 0:
        return False, "Could not find matching ')'"

    if saw_operator == True:
        return False, "Expected operand after operator!"

    return True, words


def process_calculation(expression: List[str]) -> float | int:
    # This functions evaulates the broken down expression and returns a number

    if len(expression) == 1:  # If there is only a number left, return it
        num = float(expression[0])
        return (int(num) if num.is_integer() else num)

    # If there are brackets in the expression, deal with them
    if "(" in expression:
        # Get their indexes
        br_start_index = expression.index("(")
        br_end_index = get_ending_bracket_index(expression, br_start_index)

        # Get the sub expression inside them
        sub_array = expression[br_start_index + 1: br_end_index]

        print(sub_array)  # TODO: Remove this debug print
        expression_ans = process_calculation(sub_array)

        expression = replace_array_values_with_value(expression, br_start_index, br_end_index, expression_ans)
    else:
        operator, operator_index = get_highest_operator_index(expression)

        if operator_index == -1:
            raise ValueError("Somehow there are no operators left but there are still numbers to process!", expression)

        first_operand, second_operand = float(expression[operator_index - 1]), float(expression[operator_index + 1])

        answer = calculate(operator, first_operand, second_operand)

        expression = replace_array_values_with_value(expression, operator_index - 1, operator_index + 1, answer)

    return process_calculation(expression)


if __name__ == "__main__":
    while True:

        user_input = take_input()

        if user_input == "exit":
            break

        stripped_input = user_input.strip()

        if stripped_input == "":
            continue

        statement_type = guess_statement_type(stripped_input)

        if statement_type == "assignment":
            inputValid, data = validate_assignment(user_input)
            if inputValid:
                var_name, calculation = data
                calculation_valid, words = validate_calculation(calculation)
                if calculation_valid:
                    vars[var_name] = process_calculation(replace_vars(words))
                else:
                    print(words, file=stderr)
            else:
                print(data, file=stderr)
        else:
            inputValid, words = validate_calculation(user_input)

            if inputValid:
                words = replace_vars(words)
                print(words)
                print(process_calculation(words))
            else:
                print(words, file=stderr)
