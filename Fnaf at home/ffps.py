import random

active_game_salvage = False
salvage_animatronics = {
    "Molten Freddy": {"difficulty": 0.7, "salvage_value": 100},
    "Scraptrap": {"difficulty": 0.5, "salvage_value": 150},
    "Scrap Baby": {"difficulty": 0.4, "salvage_value": 200},
    "Lefty": {"difficulty": 0.3, "salvage_value": 250}
}
taser_uses = 3

def ffps():
    global active_game_salvage, taser_uses
    active_game_salvage = True

    print("FNAF 6 Salvage Mini-Game")
    print("You will attempt to salvage an animatronic. Choose wisely!")

    # Randomly choose an animatronic to salvage
    animatronic = random.choice(list(salvage_animatronics.keys()))
    print(f"\nYou encountered {animatronic}!")

    phase = "SLEEP MODE"  # Start in Sleep Mode

    while active_game_salvage:
        print(f"\nCurrent phase: {phase}")
        action = input("Choose action (salvage/check/throw): ").strip().lower()

        if action == "throw":
            print(f"You decided to throw {animatronic} back into the alley.")
            print("You've chosen the easy way out. Expect to be fired at the end of the week for this choice.")
            active_game_salvage = False  # End the game on throw
            continue

        elif action == "check":
            if phase == "SLEEP MODE":
                print("You carefully check the animatronic...")
                phase = "ACTIVE MODE"  # Move to Active Mode
                print("The animatronic is now aware of you! It seems agitated...")
            else:
                print("You can only check the animatronic when it's in Sleep Mode!")

        elif action == "salvage":
            if phase == "ACTIVE MODE":
                print("You attempt to proceed with the salvage checklist...")
                success_chance = salvage_animatronics[animatronic]["difficulty"]
                if random.random() < success_chance:
                    salvage_value = salvage_animatronics[animatronic]["salvage_value"]
                    print(f"You successfully completed the salvage checklist!")
                    print(f"You salvaged {animatronic} for {salvage_value} points!")
                    active_game_salvage = False  # End the game on success
                else:
                    print(f"{animatronic} is becoming agitated!")
                    phase = "AGGRESSIVE MODE"  # Move to Aggressive Mode
                    if taser_uses > 0:
                        taser_action = input("The animatronic is aggressive! Use taser? (yes/no): ").strip().lower()
                        if taser_action == "yes":
                            taser_uses -= 1
                            print(f"You used the taser. Remaining uses: {taser_uses}")
                            if taser_uses == 0:
                                print("Warning: Taser is out of uses and may damage the animatronic!")
                            phase = "SLEEP MODE"  # Reset phase after using taser
                        else:
                            print(f"You hesitated and {animatronic} attacked you! Game over.")
                            active_game_salvage = False  # End the game on failure
                    else:
                        print("You have no taser uses left! The animatronic attacks!")
                        active_game_salvage = False  # End the game on failure
            else:
                print("You cannot salvage in the current phase! Check the animatronic first.")

        else:
            print("Invalid action. Type 'salvage', 'check', or 'throw'.")