import random
import time
import threading

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