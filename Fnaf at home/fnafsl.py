import random

repair_tasks = 5
mangle_distance = 0
max_mangle_distance = 3
active_game_sister_location = False

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