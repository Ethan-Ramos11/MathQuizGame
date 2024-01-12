import questionary
from termcolor import colored
import random
from queue import Queue, Empty
import threading

# Function to check if one number is divisible by
# another and ensures that the divisor is not zero


def divisible(numOne, numTwo):
    return numTwo != 0 and numOne % numTwo == 0

# Generates a pair of numbers for the math operation


def generatePair(oper):
    numOne = random.randint(0, 12)
    numTwo = random.randint(0, 12)
    # Ensure non-zero divisor for division operations
    # and the division results in a whole number
    if oper == "/":
        while not divisible(numOne, numTwo):
            numOne = random.randint(0, 12)
            numTwo = random.randint(1, 12)
    return (numOne, numTwo)

# Generates a math question and calculates the answer


def generatePrompt():
    operation = random.choice(["+", "-", "*", "/"])
    numPair = generatePair(operation)
    prompt = f"What is {numPair[0]} {operation} {numPair[1]}"
    answer = 0
    # Performs the operation based on the selected operator
    # in order to compare it to the user's answer
    if operation == "+":
        answer = numPair[0] + numPair[1]
    elif operation == "-":
        answer = numPair[0] - numPair[1]
    elif operation == "*":
        answer = numPair[0] * numPair[1]
    else:
        answer = numPair[0] / numPair[1]
    return (answer, prompt)

# Function to get user input using questionary within a separate thread


def askQuestion(prompt, queue):
    try:
        answer = questionary.text(prompt).ask()
        queue.put(int(answer))
    except ValueError:
        queue.put(None)

# Function to handle the timing of each question


def timedInput(prompt, timeout=10):
    queue = Queue()
    timedThread = threading.Thread(target=askQuestion, args=(prompt, queue))
    timedThread.daemon = True
    timedThread.start()

    # Return the input or None if timeout occurs
    try:
        return queue.get(block=True, timeout=timeout)
    except Empty:
        return None

# Main game loop


def play():

    welcomeMessage = """
Hello, this is a 10 question math quiz game.
You will have 5 seconds to answer each questions.
Press the enter key to begin
"""
    con = "y"
    questionary.text(welcomeMessage).ask()
    while con == "y":
        questions = 10
        correct = 0
        # Loops through a fixed number of questions
        while questions > 0:
            components = generatePrompt()
            guess = timedInput(components[1], timeout=5)
            # Check the answer and provide feedback
            if guess == None or guess != components[0]:
                print(colored(components[0], "white", "on_red"))
            else:
                print(colored(components[0], "white", "on_green"))
                correct += 1
            questions -= 1
        # Prints the total number of correct answers
        print(f'You got {correct} questions correct')
        # Ask the user if they want to play again
        con = questionary.rawselect(
            "Would you like to play again?",
            choices=["y", "n"]
        ).ask()
    print("Goodbye")

# Start the game
play()
