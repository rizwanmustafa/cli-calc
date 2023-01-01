from typing import Tuple, List, Dict
from sys import stderr

vars = dict()

# TODO: Ensure that there are numbers before and after the expression


def take_input():
    user_input = input(">>> ")
    return user_input


def validate_input(user_input: str) -> Tuple[bool, List[str]]:
    # This methods makes sure that only valid characters are in the user input
    # It also makes sure that the number of brackets are correct
    # The first item tells if the input is valid.
    # If the input is valid, the second item has the list of processed items
    # If the input is not valid, the second item is an empty array

    bracket_num = 0
    started_var = False
    saw_operator = False
    words = []  # This is supposed to look something like this ["$asdf", "*", "(", "2", "+", "4", ")"]
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

        if char in ["$", "("] and saw_operator == False:
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


def replace_array_values_with_value(array: List, start_index: int, end_index: int, value: any):
    for _ in range(end_index - start_index + 1):
        array.pop(start_index)

    array.insert(start_index, value)
    print(array)

    return array


def process_query(expression: List[str]) -> float:
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
        expression_ans = process_query(sub_array)

        expression = replace_array_values_with_value(expression, br_start_index, br_end_index, expression_ans)

    elif "/" in expression:
        operator_index = expression.index("/")

        first_operand = float(expression[operator_index - 1])
        second_operand = float(expression[operator_index + 1])
        answer = first_operand / second_operand

        expression = replace_array_values_with_value(expression, operator_index - 1, operator_index + 1, answer)

    elif "*" in expression:
        operator_index = expression.index("*")

        first_operand = float(expression[operator_index - 1])
        second_operand = float(expression[operator_index + 1])
        answer = first_operand * second_operand

        expression = replace_array_values_with_value(expression, operator_index - 1, operator_index + 1, answer)

    elif "+" in expression:
        operator_index = expression.index("+")

        first_operand = float(expression[operator_index - 1])
        second_operand = float(expression[operator_index + 1])
        answer = first_operand + second_operand

        expression = replace_array_values_with_value(expression, operator_index - 1, operator_index + 1, answer)

    elif "-" in expression:
        operator_index = expression.index("-")

        first_operand = float(expression[operator_index - 1])
        second_operand = float(expression[operator_index + 1])
        answer = first_operand - second_operand

        expression = replace_array_values_with_value(expression, operator_index - 1, operator_index + 1, answer)

    return process_query(expression)


def replace_vars(words: List[str]) -> List[str]:
    global vars
    for index, value in enumerate(words):
        if "$" in value:
            words[index] = vars.get(value, "1")  # TODO: Remove this replace with 1 and instead raise an error

    return words


arr = ["2", "(", "2", "*", "(", "2", "+", "2", ")", ")"]
print("".join(arr))

while True:

    user_input = take_input()

    if user_input.strip() == "exit":
        break

    inputValid, words = validate_input(user_input)

    if inputValid:
        words = replace_vars(words)
        print(words)
        print(process_query(words))
    else:
        print(words, file=stderr)
