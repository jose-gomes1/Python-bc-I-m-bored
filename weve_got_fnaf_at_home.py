import random
import time
import sys
import threading
import os

# Global variables for FNAF 1
active_game = False
power_level = 100  # Power starts at 100%
right_door_closed = False
left_door_closed = False
action_count = 0  # To count the number of actions taken (representing hours)
animatronics = {
    "Bonnie": {"aggression": random.randint(15, 20), "location": "left", "checked": False},
    "Chica": {"aggression": random.randint(15, 20), "location": "right", "checked": False},
    "Foxy": {"aggression": random.randint(10, 14), "location": "left", "checked": False},
    "Freddy": {"aggression": random.randint(5, 9), "location": "camera", "checked": False},
    "Golden Freddy": {"aggression": random.randint(1, 4), "location": "camera", "checked": False}
}

# Global variables for FNAF 2
player_health = 100
player_max_health = 200
animatronic_health = {
    "Toy Bonnie": 50,
    "Toy Chica": 50,
    "Toy Freddy": 50,
    "Mangle": 60,
    "Balloon Boy": random.choice([40, 500])
}
current_enemy = None
player_turn = True
healed = False

# Global variables for FNAF 3
lures_used = 0
audio_rebooting = False
springtrap_moves = 0  # Track the number of successful Springtrap movements
max_springtrap_moves = random.randint(4, 10)  # Number of moves before Springtrap wins

# Global variables for FNAF 4
flashlight_flashes = 4
nightmarionne_position = 0
max_nightmarionne_moves = 5
max_player_actions = 10
player_actions = 0

# Global variables for Sister Location
repair_tasks = 5
mangle_distance = 0
max_mangle_distance = 3
active_game_sister_location = False

# Global variables for the salvage mini-game
active_game_salvage = False
salvage_animatronics = {
    "Molten Freddy": {"difficulty": 0.7, "salvage_value": 100},
    "Scraptrap": {"difficulty": 0.5, "salvage_value": 150},
    "Scrap Baby": {"difficulty": 0.4, "salvage_value": 200},
    "Lefty": {"difficulty": 0.3, "salvage_value": 250}
}
taser_uses = 3

def display_menu():
    print("==================================================")
    print("Welcome to the Five Nights at Freddy's Mini-Games!")
    print("Choose your mode:")
    print("1. Fnaf 1")
    print("2. Punch 2 Fnaf")
    print("3. Frights")
    print("4. Nightmare")
    print("5. Vent Repair")
    print("6. Salvage")
    print("0. Exit")
    print("==================================================")

def timed_input(prompt, timeout=5):
    response = [None]  # Use a list to hold the response as Python does not allow variable assignment in nested functions.
    
    # Function to capture input
    def get_input():
        response[0] = input(prompt)
    
    # Start the input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True  # Set as daemon so it won't block the program from exiting
    input_thread.start()
    
    # Wait for the thread to finish or timeout
    input_thread.join(timeout)
    
    # If the thread is still active after the timeout, it means the user didn't input in time
    if input_thread.is_alive():
        return None  # Return None if the timeout occurs and no input was given
    
    return response[0]  # Return the actual response if input was provided in time

def get_timeout(aggression, max_time=20):
    return max(7.5, max_time - aggression)

def reset_game():
    global power_level, right_door_closed, left_door_closed, action_count, hp
    power_level = 100
    right_door_closed = False
    left_door_closed = False
    action_count = 0
    hp = 2

def fnaf1():
    global active_game, power_level, right_door_closed, left_door_closed, action_count, animatronics, hp
    active_game = True
    power_level = 100
    right_door_closed = False
    left_door_closed = False
    action_count = 0  # Reset action count
    hp = 2

    reset_game()

    print("FNAF 1 Mini Game\nThe night is starting...\nYou can use right to close the right door, left to close the left door and check to check the cameras")

    while active_game and power_level > 0 and action_count < 12:
        if action_count % 2 == 0 and action_count > 0:
            print(int(action_count / 2), "AM")
        time.sleep(2)  # Simulate time passing (2 seconds per turn)
        action_count += 1

        # Drain power if doors are closed
        if right_door_closed or left_door_closed:
            power_level -= 5
            print(f"Power level: {power_level}%")

        # Random event: animatronic appears
        if random.random() < 0.4:  # 40% chance of animatronic appearing
            animatronic = random.choice(list(animatronics.keys()))
            aggression = animatronics[animatronic]["aggression"]
            location = animatronics[animatronic]["location"]
            print(f"Danger! {animatronic} is approaching with aggression level {aggression}.")

            # Player's response to animatronics
            if animatronic == "Freddy":
                response = timed_input("Freddy is coming: ", timeout=get_timeout(aggression))
                if response == 'check':
                    print("You checked the cameras and saw Freddy. You're safe for now.")
                    animatronics["Freddy"]["checked"] = True
                else:
                    print("That's not the correct action against Freddy! He's comming closer...")
                    hp -= 1

            elif animatronic == "Chica":
                response = timed_input("Chica is coming: ", timeout=get_timeout(aggression))
                if response == 'right':
                    right_door_closed = True
                    print("You closed the right door. Chica is sent back.")
                else:
                    print("That's not the correct action against Chica! She's coming closer...")
                    hp -= 2

            elif animatronic == "Bonnie":
                response = timed_input("Bonnie is coming: ", timeout=get_timeout(aggression))
                if response == 'left':
                    left_door_closed = True
                    print("You closed the left door. Bonnie is sent back.")
                else:
                    print("That's not the correct action against Bonnie! He's coming closer...")
                    hp -= 2

            elif animatronic == "Foxy":
                response = timed_input("Foxy needs to be checked: ", timeout=get_timeout(aggression))
                if response == 'check':
                    print("You checked the cameras and saw Foxy. You're safe for now.")
                    animatronics["Foxy"]["checked"] = True
                else:
                    print("That's not the correct action against Foxy! He's running down the left hall.")
                    response = timed_input("Quick! Close your door: ", timeout=get_timeout(aggression))
                    if response == 'left':
                        left_door_closed = True
                        print("You closed the left door. Foxy is sent back.")
                    else:
                        left_door_closed = False
                        print("Foxy got to you.")
                        hp -= 2

            elif animatronic == "Golden Freddy":
                response = timed_input("Golden Freddy is coming: ", timeout=get_timeout(aggression))
                if response == 'check':
                    print("You checked the cameras and saw Golden Freddy. You survived this time.")
                    animatronics["Golden Freddy"]["checked"] = True
                else:
                    print("That's not the correct action against Golden Freddy! He remains a mystery...")
                    hp -= 1

        # Check if HP has reached 0
        if hp <= 0:
            print("Game over! You got jumpscared.")
            active_game = False
            break

        # If power runs out during the game loop
        if power_level <= 0:
            print("Power is out! Freddy will try to get you...")
            if random.random() < 0.5:
                print("You managed to survive the night!")
            else:
                print("Freddy got you. Game over.")
            active_game = False
            break

    if action_count >= 12:
        print("Congratulations! You survived the night.")

    active_game = False

def fnaf2():
    global active_game, player_health, current_enemy, player_turn, healed
    active_game = True
    player_health = 100
    player_max_health = 200
    player_turn = True
    healed = False  # Reset healed status

    print("FNAF 2 Toy Animatronic Turn-Based Battle Mini-Game\nType 'attack' to attack or 'heal' to heal yourself!")

    current_enemy = random.choice(list(animatronic_health.keys()))
    print(f"Your opponent: {current_enemy}. Health: {animatronic_health[current_enemy]}")

    while active_game and player_health > 0:
        action = input("Your action: ").strip().lower()
        if action == 'attack':
            damage = random.randint(10, 40)
            # Deal 10 times damage if attacking Balloon Boy with 500 HP
            if current_enemy == "Balloon Boy" and animatronic_health[current_enemy] == 500:
                damage *= 20

            animatronic_health[current_enemy] -= damage
            # Player heals for the amount of damage dealt to the animatronic
            player_health = min(player_health + damage, player_max_health)

            print(f"You attacked {current_enemy} for {damage} damage and healed yourself for {damage} health!")
            print(f"Your Health: {player_health}")

            if animatronic_health[current_enemy] <= 0:
                print(f"You defeated {current_enemy}!")
                await_next_enemy()
            else:
                print(f"{current_enemy}'s Health: {animatronic_health[current_enemy]}")

            animatronic_attack()
        elif action == 'heal':
            player_health = player_max_health
            healed = True  # Set healed to True when heal command is used
            print(f"You fully healed yourself! Current Health: {player_health}")
            animatronic_attack()
        else:
            print("Invalid action. Type 'attack' or 'heal'.")

        if player_health <= 0:
            print("You've been defeated! Game over.")
            active_game = False


def animatronic_attack():
    global active_game, player_health, current_enemy
    if not active_game:
        return
    damage = random.randint(1, 45)
    player_health -= damage
    print(f"{current_enemy} attacks you for {damage} damage! Your Health: {player_health}")
    if player_health <= 0:
        print("You've been defeated! Game over.")
        active_game = False


def await_next_enemy():
    global active_game, current_enemy
    remaining_enemies = [enemy for enemy in animatronic_health if animatronic_health[enemy] > 0]
    if not remaining_enemies:
        print("Congratulations! You have defeated all animatronics!")
        active_game = False
    else:
        current_enemy = random.choice(remaining_enemies)
        print(f"Your next opponent: {current_enemy}. Health: {animatronic_health[current_enemy]}")


def fnaf3():
    global active_game, power_level, lures_used, audio_rebooting, springtrap_moves
    active_game = True
    power_level = 100
    lures_used = 0
    audio_rebooting = False
    springtrap_moves = 0
    action_count = 0  # To track the number of actions taken
    max_springtrap_moves = 4  # Maximum moves Springtrap can make before catching the player
    lure_reboot_threshold = random.randint(3, 5)  # Random threshold for audio reboot

    print("FNAF 3 Springtrap Encounter Mini-Game")
    print("Survive until 6 AM!")

    while active_game and power_level > 0:
        action = input("Choose action (check/lure): ").strip().lower()
        action_count += 1  # Increment action count

        # Display the current hour every two actions
        if action_count % 2 == 0:  # Check if it's an even action count
            print(int(action_count / 2), "AM")  # Display the hour

        if action == "check":
            print("You checked the cameras and saw Springtrap. He is moving...")
            springtrap_moves += 1
            if springtrap_moves >= max_springtrap_moves:
                print("Springtrap caught you! Game over.")
                active_game = False

        elif action == "lure":
            if audio_rebooting:
                print("Audio is currently rebooting. You cannot use the lure until reboot is complete.")
                continue

            # 50% chance that Springtrap follows the lure
            if random.random() < 0.5:
                print("Springtrap followed the lure and was sent back!")
                springtrap_moves -= 1
            else:
                print("Springtrap did not follow the lure and is still approaching!")
                springtrap_moves += 1

            # Check if the player has successfully lured Springtrap back
            if springtrap_moves < 0:
                springtrap_moves = 0  # Prevent negative moves

            lures_used += 1  # Increment the lure count

            # Check if lures used has reached the random threshold
            if lures_used >= lure_reboot_threshold:
                print("Audio needs to be rebooted after using", lure_reboot_threshold, "lures.")
                audio_rebooting = True
                for _ in range(2):  # Simulate reboot time
                    time.sleep(1)
                    springtrap_moves += 1  # Springtrap moves closer during reboot
                    print("Audio reboot in progress... Springtrap is moving!")
                audio_rebooting = False
                lures_used = 0  # Reset lures used
                lure_reboot_threshold = random.randint(3, 5)  # Set a new random threshold

        # Check if the player has survived until 6 AM
        if action_count >= 12:  # 12 actions corresponds to 6 AM
            print("You've survived until 6 AM! You win!")
            active_game = False

        # If Springtrap reaches the player, it's game over
        if springtrap_moves >= max_springtrap_moves:
            print("Springtrap caught you! Game over.")
            active_game = False


def fnaf4():
    global active_game, flashlight_flashes, nightmarionne_position, player_actions
    active_game = True
    flashlight_flashes = 4
    nightmarionne_position = 0
    player_actions = 0

    print("FNAF 4 Nightmare Encounter Mini-Game")
    while active_game:
        action = input("Choose action (flash/wait): ").strip().lower()
        if action == "flash":
            if flashlight_flashes > 0:
                flashlight_flashes -= 1
                nightmarionne_position = 0
                print(f"Nightmarionne has been sent back! Flashes remaining: {flashlight_flashes}")
            else:
                print("No flashlight flashes remaining!")
        elif action == "wait":
            player_actions += 1
            nightmarionne_position += 1
            print(f"Nightmarionne is now at position {nightmarionne_position}. Actions remaining: {max_player_actions - player_actions}")

            if nightmarionne_position >= max_nightmarionne_moves:
                print("Nightmarionne reached your location. You've been caught! Game over.")
                active_game = False

            if player_actions >= max_player_actions:
                print("The night is over. You won!")
                active_game = False
        else:
            print("Invalid action. Type 'flash' or 'wait'.")

def fnafsl():
    global active_game_sister_location, repair_tasks, mangle_distance
    active_game_sister_location = True
    repair_tasks = 5
    mangle_distance = 0

    print("Sister Location Vent Repair Mini-Game")
    print("Repair the vents while keeping Mangle at bay!")

    while active_game_sister_location and repair_tasks > 0:
        action = input("Choose action (repair/check): ").strip().lower()

        if action == "repair":
            if random.random() < 0.45:  # 45% chance to successfully repair
                repair_tasks -= 1
                print(f"Repair successful! Tasks remaining: {repair_tasks}")
            else:
                print("Repair failed! Mangle is getting closer.")
                mangle_distance += 1

        elif action == "check":
            if mangle_distance > 0:
                print("You checked the vents and saw Mangle. She has been pushed back.")
                mangle_distance -= 1
            else:
                print("The vents are clear. No sign of Mangle.")

        else:
            print("Invalid action. Type 'repair' or 'check'.")

        # Check if Mangle has reached the player
        if mangle_distance >= max_mangle_distance:
            print("Mangle got to you! Game over.")
            active_game_sister_location = False
            break

    if repair_tasks == 0:
        print("Congratulations! You successfully repaired the vents and survived!")

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

def main():
    while True:
        time.sleep(1.5)
        os.system("clear || cls")
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            fnaf1()
        elif choice == '2':
            fnaf2()
        elif choice == '3':
            fnaf3()
        elif choice == '4':
            fnaf4()
        elif choice == '5':
            fnafsl()
        elif choice == '6':
            ffps()
        elif choice == '0':
            print("Exiting the game. Goodbye!")
            sys.exit()  # Exit the program
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

# To add:
# think about it later
