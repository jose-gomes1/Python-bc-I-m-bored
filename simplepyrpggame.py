import random

def player():
    name = input("Hello adventurer, please insert your name: ")
    print(f"Hello, {name}\nA monster appeared!\n")
    return name

def monster():
    monster_name = input("Choose its name: ")
    monster_lvl = random.randint(1, 5)
    monster_hp = random.randint(1 * monster_lvl, 5 * monster_lvl)
    return monster_name, monster_hp, monster_lvl

def fight(monster_name, monster_hp, monster_lvl):
    player_hp = 10  # Initialize player health
    print(f"You have {player_hp} HP.")

    while True:
        print(f"\nThe monster {monster_name} LVL: {monster_lvl} has {monster_hp} HP!\nWhat will you do?\n'attack' to attack, 'run' to run away")
        
        action = input("> ").lower()
        
        if action == "attack":
            # Simulate player attack damage
            damage = random.randint(1, 15)
            monster_hp -= damage
            print(f"You dealt {damage} damage to {monster_name}!")
            
            # Check if the monster is defeated
            if monster_hp <= 0:
                print(f"{monster_name} was defeated!")
                break  # End fight when monster is defeated
            else:
                print(f"The monster {monster_name} has {monster_hp} HP remaining.")

            # Monster attacks back
            monster_damage = random.randint(1, 2) +  (monster_lvl - 1)  # Monster damage
            player_hp -= monster_damage
            print(f"The monster {monster_name} attacks you and deals {monster_damage} damage!")
            print(f"You have {player_hp} HP remaining.")

            # Check if player is defeated
            if player_hp <= 0:
                print("You have been defeated by the monster!")
                break  # End game if player is defeated
        
        elif action == "run":
            num = random.randint(1, 5)
            if num >= 3:
                print("You ran away from the monster!")
                break  # End the fight if the player runs away
            else:
                print("You were unable to run")

        else:
            print("Invalid action. Please type 'attack' or 'run'.")

# Game logic
player_name = player()  # Get player's name
monster_name, monster_hp, monster_lvl = monster()  # Get monster details
fight(monster_name, monster_hp, monster_lvl)  # Start fight with the monster
