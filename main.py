from src.core import Core

def main():
    number1 = random.randint(0, 9)
    number2 = random.randint(0, 9)

    answer = input(f"{number1} + {number2} = ? ")

    try:
        answer = int(answer)
        if answer == number1 + number2:
            print("Correct!")
        else:
            print(f"Incorrect! Correct answer: {number1 + number2}")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()