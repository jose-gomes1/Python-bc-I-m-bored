import random
import time

lures_used = 0
audio_rebooting = False
springtrap_moves = 0  # Track the number of successful Springtrap movements
max_springtrap_moves = random.randint(4, 10)  # Number of moves before Springtrap wins

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