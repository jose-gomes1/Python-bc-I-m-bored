flashlight_flashes = 4
nightmarionne_position = 0
max_nightmarionne_moves = 5
max_player_actions = 10
player_actions = 0

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
