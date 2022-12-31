from typing import Tuple, List, Dict


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

        if started_var == False or (started_var == True and char.isalnum() == False):
            append_curr_word()

        if char in ["$", "("] and saw_operator == False:
            words.append("*")

        if char.isalnum():
            saw_operator = False
            if started_var == False and char.isnumeric() == False:
                return False, f"Unexpected character '{char}' at index {index}. If you wanted to use a variable, please remember to use the '$' at the start.", []
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
                return False, f"Unexpected character ')' at index {index}!", []

        elif char == "$":
            started_var = True
            curr_word += char
        else:
            return False, f"Unexpected character '{char}' at index {index}!", []

        # If the character we saw was not an operator, update the variables
        if char not in ["+", "*", "-", "/"]:
            saw_operator = False

    if curr_word != "":
        words.append(curr_word)

    if bracket_num != 0:
        return False, "Could not find matching ')'", []

    if saw_operator == True:
        return False, "Expected operand after operator!", []

    return True, words


def process_query(processed_input: List[str], var_dict: Dict[str, int]) -> int:

    pass


while True:
    user_input = take_input()

    if user_input.strip() == "exit":
        break

    print(validate_input(user_input))
