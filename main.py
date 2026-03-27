import csv
import random
import os

# 1. Load the flashcards from CSV
def load_flashcards(filename="acronyms.csv"):
    flashcards = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)          # Reads the header row automatically
        for row in reader:
            flashcards.append({
                "acronym": row["acronym"].strip(),
                "full_name": row["full_name"].strip(),
                "description": row["description"].strip()
            })
    return flashcards

# 2. Show a single flashcard (like a physical card)
def show_card(card):
    print("\n" + "="*50)
    print(f"ACRONYM: {card['acronym']}")
    input("\nPress ENTER to reveal the full name and description...")
    print(f"FULL NAME: {card['full_name']}")
    print(f"DESCRIPTION: {card['description']}")
    print("="*50)

# 3. Main program loop
def main():
    if not os.path.exists("acronyms.csv"):
        print("Error: acronyms.csv not found!")
        return
    
    flashcards = load_flashcards()
    print(f"Loaded {len(flashcards)} flashcards! 🎉\n")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Review all cards in order")
        print("2. Random quiz mode")
        print("3. Exit")
        
        choice = input("Enter 1, 2, or 3: ").strip()
        
        if choice == "1":
            for card in flashcards:
                show_card(card)
        elif choice == "2":
            random.shuffle(flashcards)
            for card in flashcards:
                show_card(card)
        elif choice == "3":
            print("Thanks for studying! See you next time 👋")
            break
        else:
            print("Invalid choice, please try again.")

# This runs the program when you type: python main.py
if __name__ == "__main__":
    main()