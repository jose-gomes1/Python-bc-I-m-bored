import random

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