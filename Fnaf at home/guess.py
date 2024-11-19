import random

fnaf = [
    "Freddy Fazbear", "Bonnie", "Chica", "Foxy", "Golden Freddy", "Springtrap",
    "Ballora", "Circus Baby", "Ennard", "Molten Freddy", "Scrap Baby", "Scraptrap",
    "Dark Springtrap", "Lefty", "Rockstar Freddy", "Rockstar Bonnie", "Rockstar Chica",
    "Rockstar Foxy", "Carnie", "Happy Frog", "Mr. Hippo", "Orville Elephant",
    "Nedd Bear", "Pigpatch", "Funtime Freddy", "Funtime Foxy", "Funtime Chica", "Nightmare",
    "Nightmare Fredbear", "Nightmare Freddy", "Nightmare Bonnie", "Nightmare Chica",    
    "Nightmare Foxy", "Nightmare Mangle", "Nightmare Balloon Boy", "Phantom Freddy",
    "Phantom Chica", "Phantom Foxy", "Phantom Balloon Boy", "Phantom Puppet",
    "Phantom Mangle", "Shadow Freddy", "RWQFSFASXC", "Helpy",
    "Dee Dee", "XOR", "Old Man Consequences", "Vengeful Spirit",
    "Toy Freddy", "Toy Chica", "Toy Bonnie", "Mangle", "Balloon Boy", "Puppet",
    "JJ", "Withered Freddy", "Withered Bonnie", "Withered Chica", "Withered Foxy",
    "Withered Golden Freddy", "Bidibab", "Electrobab", "Minireena", "Bon Bon",
    "Bonnet", "Yenndo", "Music Man", "Glamrock Freddy", "Glamrock Chica",
    "Montegomery Gator", "Roxanne Wolf", "DJ Music Man", "Wind-Up Music Man",
    "Glitchtrap", "Dreadbear", "Vanny", "Helpi", "Burntrap", "Tangle", "Sun", "Moon",
    "STAFF Bot", "Map Bot", "Mask Bot", "The Mimic", "Shattered Roxy", "Shattered Monty",
    "Shattered Chica", "Glamrock Bonnie", "MXES", "Ruined Chica", "Ruined Roxy", "Ruined Monty",
    "Ruined DJ Music Man", "Ruined Wind-Up Music Man", "Nightmare Staff Bot", 
    "Jack-O-Chica", "Jack-O-Bonnie", "Nightmarionne", "Plushtrap", "Security Puppet", "Captain Foxy",
    "Jack-O-Moon", "Eclipse", "Ruined Freddy", "Springbonnie", "Fredbear", "Mystic Hippo", "Wet Floor Bot",
    "Freddy Frostbear", "8-Bit Baby", "Endo-01", "Endo-02", "Nightmare Endo", "Glamrock Endo", "Freddles",
    "Grimm Foxy", "Lolbit", "Lemonade Clown", "Fruit Punch Clown", "Jackie", "Head Chef Bot", "Hand Unit",
    "Mr Cupcake", "Nightmare Cupcake", "Jack-O-Lantern", "Hand Unit", "Dark Freddy", "Neon Bonnie", "Neon Chica",
    "Burnt Foxy", "Shadow Mangle", "Dark Foxy", "Party Freddy", "Bucket Bob", "Mr Can-Do", "Number 1 Crate", "Pan Stan",
    "Paper Pals", "Candy Cadet", "El Chip", "Tilt", "Phone Guy", "Phone Dude", "Gregory", "Vanessa", "Michael Afton", 
    "Cassie", "Jeremy Fitzgerald", "Elizabeth Afton", "William Afton", "Crying Child"
]

def guess():
    # Initialize game variables
    chosen_name = random.choice(fnaf).lower()  # Choose random animatronic
    guessed_letters = set()  # Track letters guessed by the player
    attempts = 7  # Number of allowed wrong guesses
    active_game = True

    # Prepare display with underscores and spaces for multi-word names
    display = ["_" if char.isalpha() else char for char in chosen_name]

    print("Welcome to the FNAF Guessing Game!")
    print("Guess the character's name:")
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
                # Update display with correctly guessed letter
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
            print(f"Game over! The character was: {chosen_name.title()}")
            active_game = False