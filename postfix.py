# postfix.py (main program file)
# Jonathan Grant
# 2016.04.10
# This menu-driven program translates infix notation expressions
# into postfix notation expressions.
# The user can enter their own expression (assumed to be correct),
# or the user can choose to have the program read from a text file
# containing expressions.

from cs_stack import Stack

# Functions

def print_instructions():
    """ Prints instructions. """

    print()
    print('Instructions')
    print()
    print('This menu-driven program translates')
    print('infix notation expressions into postfix')
    print('notation expressions. You can enter your')
    print('own expression (assumed to be correct), by')
    print('entering choice 3. You can also choose to')
    print('have the program read from a text file')
    print('containing test expressions by entering')
    print('choice 2.')
    print()


def translate(infix_expression):
    """ Translates an infix expression to postfix.

    Uses a stack to store various characters,
    such as operators and parentheses.

    infix_expression - String infix expression, ex. 3 + 4 + 5

    Example of a translation:

    infix:   (3 + 4) * 5
    postfix: 3 4 + *
    """

    # stack - Stack object of size 50
    # postfix_expression - List that operators and digits
    #                      append to in order to create a
    #                      postfix expression

    stack = Stack(50)

    postfix_expression = []

    # Analyze each character in the
    # infix expression, from left to right
    for char in infix_expression:

        # Copy any digit to the output
        if char.isdigit():

            postfix_expression.append(char)

        # Ignore spaces in the infix expression.
        # This means there will be no spacing in the
        # postfix expression.
        elif char.isspace():

            pass

        # Check if the character in question
        # is an operator
        elif is_operator(char):

            if associativity(char) == 'left':

                # If it is a left associative operator, copy the
                # operator on top of the stack to the output as long
                # as it has an equal or greater value than the left
                # associative operator in question.
                while (not stack.is_empty() and
                precedence(stack.peek()) >=
                precedence(char)):

                    postfix_expression.append(stack.pop())

                stack.push(char)

            # If the operator is right associative, push
            # it to the stack.
            else:

                stack.push(char)

        elif char == '(':

            # Always push left parenthesis
            stack.push('(')

        elif char == ')':

            # Pop/copy any operators inside the
            # complete set of parentheses
            while stack.peek() != '(':

                postfix_expression.append(stack.pop())

            # Then delete the
            # corresponding open parenthesis
            # that remains in the stack
            stack.pop()

        else:

            print('ERROR')

    # After looking at every character in the
    # infix expression, pop the stack and copy the
    # operators to the output until the stack is empty.
    while not stack.is_empty():

        postfix_expression.append(stack.pop())

    return postfix_expression


def is_operator(character):
    """ Finds if character in question is an operator. """

    operators = ['+', '-', '*', '/', '^']

    return character in operators


def associativity(operator):
    """ Defines the associativity for each operator.

    operator - Character in question (+, -, *, /, ^)

    '+', '-', '*', and '/' are all left associative.
    '^' is the only right associative operator.
    """

    # associativity - A string value, either 'left' or 'right'

    left_associative_ops = ['+', '-', '*', '/']

    # Note:
    # A list for right associative operators
    # is not needed, since we know that they
    # must be right associative if they are
    # not left associative.

    if operator in left_associative_ops:

        associativity = 'left'

    else:

        associativity = 'right'

    return associativity


def precedence(operator):
    """ Defines the precedence for each operator.

    Precedence is needed for creating an
    "order of operations" or PEMDAS system
    for postfix expressions.
    """

    if operator == '(':

        precedence = 0

    elif operator == '+' or operator == '-':

        precedence = 1

    elif operator == '*' or operator == '/':

        precedence = 2

    else:

        precedence = 3

    return precedence


def do_test_file():
    """ Recieves infix expressions from a test text file to read."""

    print("\nNote that the test file must .txt in the same directory as this")
    print("program, and only contain infix expressions.")

    file_name = input("\nName of test file: ")

    with open(file_name) as infix_file:

        # Each line in the file is a separate infix
        # expression that is to be translated to postfix.
        for line in infix_file:

            postfix_expression = translate(line)

            # Print each postfix expression on a new line,
            # matching the format of the test file.
            print_expressions(line, postfix_expression)

def input_infix_expression():
    """ Allows the user to enter an infix expression.

    Note: The expression is assumed to be syntactically correct.
    """

    print()
    input_expression = input('Infix expression:   ')

    # Returns the expression without the new line
    # character at the end
    return input_expression.rstrip('\n')

def do_user():
    """ Translates a user-input infix expression."""

    repeat = True

    while repeat:

        infix_expression = input_infix_expression()

        postfix_expression = translate(infix_expression)

        print_expressions(infix_expression, postfix_expression)

        answer = input('\nTry again (y/n)? ')

        if answer != 'y' and answer != 'Y':

            repeat = False

        print()

def print_expressions(infix_expression, postfix_expression):
    """ Prints the infix and corresponding postfix expression. """

    print()
    print('Infix expression:  ', infix_expression)
    print('Postfix expression: ', end = '')

    # Since the postfix_expression is a list,
    # printing each character will prevent
    # printing a list's brackets and quotes.
    for char in postfix_expression:

        print(char, end = '')

    print()
    print()

def print_menu():
    """ Prints a menu screen. """

    print('1) Display instructions')
    print('2) Read from test file')
    print('3) Enter your own infix expression')
    print('4) Quit')
    print()

def do_menu():
    """ Allows the user to choose menu items. """

    # choice - Integer that corresponds to menu items

    print_menu()

    # Choice is set to 1 by default to enter the
    # menu loop.
    choice = 1

    # Keep running the program until the user
    # decides to quit.
    while choice != 4:

        choice = int(input('What is your choice (1-4)? '))

        if choice == 1:

            print_instructions()

        elif choice == 2:

            do_test_file()

        elif choice == 3:

            do_user()

        elif choice == 4:

            pass

        else:

            print('\nPlease choose a valid input from 1-4.\n')

        # Prevent from showing the menu right before
        # the program ends if the user chooses to quit.
        if choice != 4:

            print_menu()


def Main():
    """ Displays a menu and executes corresponding instructions. """

    print('\nInfix to Postfix Translator\n')

    do_menu()

Main()
