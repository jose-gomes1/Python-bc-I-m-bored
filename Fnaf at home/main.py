import time
import sys
import os
import fnafs

def main():
    while True:
        time.sleep(1.5)
        os.system("clear || cls")
        fnafs.menu.display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            fnafs.fnaf1.fnaf1()
        elif choice == '2':
            fnafs.fnaf2.fnaf2()
        elif choice == '3':
            fnafs.fnaf3.fnaf3()
        elif choice == '4':
            fnafs.fnaf4.fnaf4()
        elif choice == '5':
            fnafs.fnafsl.fnafsl()
        elif choice == '6':
            fnafs.ffps.ffps()
        elif choice == '7':
            fnafs.guess.guess()
        elif choice == '0':
            print("Exiting the game. Goodbye!")
            sys.exit()  # Exit the program
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()