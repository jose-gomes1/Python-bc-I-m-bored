import random

books = [
    "Silver Eyes", "Twisted Ones", "Fourth Closet", #Novel Trilogy
    "Into the Pit", "Fetch", "1:35 AM", "Step Closer", "Bunny Call", "Blackbird", 
    "The Cliff", "Gumdrop Angel", "The Puppet Carver", "Friendly Face", "Prankster", "Felix the Shark", #Fazbear Frights
    "Lally's Game", "HAPPS", "Somniphobia", "Submechanophobia",
    "The Bobbiedots Conclusion", "Nexie", "Tiger Rock", "B7-2", #Tales from the Pizzaplex
    "The Official Movie Novel", #Movie
    "VIP", "The Week Before", "Return to the Pit", "Escape the Pizzaplex", #Interactive Novel Series
    "The Freddy Files", "The Freddy Files: Updated Edition", "The Freddy Files: The Ultimate Guide",
    "Security Breach Files", "Security Breach Files: Updated Edition", #Freddy Files
    "Character Encyclopedia", "Survival Logbook" #Character Encyclopedia and Logbook
]

trilogy = [
    "Silver Eyes", "Twisted Ones", "Fourth Closet"
]

frights = [
    "Into the Pit", "Fetch", "1:35 AM", "Step Closer", "Bunny Call", "Blackbird", 
    "The Cliff", "Gumdrop Angel", "The Puppet Carver", "Friendly Face", "Prankster", "Felix the Shark"
]

tales = [
    "Lally's Game", "HAPPS", "Somniphobia", "Submechanophobia",
    "The Bobbiedots Conclusion", "Nexie", "Tiger Rock", "B7-2"
]

files = [
    "The Freddy Files", "The Freddy Files: Updated Edition", "The Freddy Files: The Ultimate Guide",
    "Security Breach Files", "Security Breach Files: Updated Edition"
]

interactive = [
    "VIP", "The Week Before", "Return to the Pit", "Escape the Pizzaplex"
]

def play_guessing_game(book_list):
    chosen_name = random.choice(book_list).lower()  # Choose random book
    guessed_letters = set()  # Track guessed letters
    attempts = 7  # Number of wrong guesses allowed
    active_game = True

    # Prepare display
    display = ["_" if char.isalpha() else char for char in chosen_name]

    print("\nWelcome to the FNAF Book Guessing Game!")
    print("Guess the book's name:")
    print(" ".join(display))

    while active_game:
        # Display current progress
        print("\nCurrent name: " + " ".join(display))
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        print(f"Remaining attempts: {attempts}")

        # Player input
        guess = input("Guess a letter or the full name: ").lower()

        # If the player guesses the full name
        if guess == chosen_name:
            print(f"Congratulations! You guessed it: {chosen_name.title()}")
            active_game = False
            break

        # If the player guesses a letter
        elif len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print(f"You already guessed '{guess}'. Try again!")
            elif guess in chosen_name:
                print(f"Good guess! '{guess}' is in the name.")
                guessed_letters.add(guess)
                # Update display
                for idx, char in enumerate(chosen_name):
                    if char == guess:
                        display[idx] = guess
            else:
                print(f"Sorry, '{guess}' is not in the name.")
                guessed_letters.add(guess)
                attempts -= 1

        else:
            print("Invalid input. Please guess a single letter or the full name.")

        # Check if the player has won
        if "_" not in display:
            print(f"Congratulations! You guessed it: {chosen_name.title()}")
            active_game = False

        # Check if the player has run out of attempts
        if attempts == 0:
            print(f"Game over! The book was: {chosen_name.title()}")
            active_game = False

def choose_category():
    print("\nChoose a category:")
    print("1. Novel Trilogy")
    print("2. Fazbear Frights")
    print("3. Tales from the Pizzaplex")
    print("4. Freddy Files")
    print("5. Interactive Novels")
    print("6. All Books")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        play_guessing_game(trilogy)
    elif choice == "2":
        play_guessing_game(frights)
    elif choice == "3":
        play_guessing_game(tales)
    elif choice == "4":
        play_guessing_game(files)
    elif choice == "5":
        play_guessing_game(interactive)
    elif choice == "6":
        play_guessing_game(books)
    else:
        print("Invalid choice. Please try again.")
        choose_category()