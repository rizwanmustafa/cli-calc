from typing import Tuple, List


def take_input():
    user_input = input(">>> ")
    return user_input


def validate_input(user_input: str) -> Tuple[bool, List[str]]:
    # This methods makes sure that only valid characters are in the user input
    # It also makes sure that the number of brackets are correct
    # The first item tells if the input is valid.
    # If the input is valid, the second item has the new modded user input
    # If the input is not valid, the second item has the error

    bracket_num = 0
    started_var = False
    saw_operator = False
    new_input = ""

    words = []  # This is supposed to look something like this ["$asdf", "*", "(", "2", "+", "4", ")"]
    curr_word = ""

    for index, char in enumerate(user_input):
        if char == " ":
            # The variable declaration has finished
            started_var = False

            # Append the current word
            if curr_word != "":
                words.append(curr_word)
                curr_word = ""

        elif char.isalnum():
            saw_operator = False
            if started_var == False and char.isnumeric() == False:
                return False, f"Unexpected character '{char}' at index {index}. If you wanted to use a variable, please remember to use the '$' at the start."
            curr_word += char

        elif char in ["+", "*", "-", "/"]:
            saw_operator = True
            if curr_word != "":
                words.append(curr_word)
                curr_word = ""
            words.append(char)

        elif char in ["(", ")"]:
            # The variable declaration has finished
            started_var = False
            if curr_word != "":
                words.append(curr_word)
                curr_word = ""

            if char == "(":
                bracket_num += 1
                if saw_operator == False:
                    new_input += " * "
                    words.append("*")
            else:
                bracket_num -= 1

            words.append(char)

            if bracket_num < 0:
                return False, f"Unexpected character ')' at index {index}!"

        elif char == "$":
            started_var = True
            saw_operator = False
            if curr_word != "":
                words.append(curr_word)
                curr_word = ""
            curr_word += char
        else:
            return False, f"Unexpected character '{char}' at index {index}!"

        new_input += char
    if curr_word != "":
        words.append(curr_word)

    print(words)

    return True, new_input


while True:
    user_input = take_input()

    if user_input.strip() == "exit":
        break

    print(validate_input(user_input))
