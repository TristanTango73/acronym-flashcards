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

# 2. Enter to continue or Esc to go back to menu
def read_enter_or_esc():
    """
    Wait for one key.
    Returns 'enter' or 'esc'.
    Other keys are ignored.
    """
    try:
        import msvcrt   # Windows
        while True:
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                return "enter"
            if ch == '\x1b':        # ESC
                return "esc"
            # arrow keys send a prefix + a second code; skip the extra
            if ch in ("\x00", "\xe0"):
                msvcrt.getwch()
    except ImportError:
        import sys, tty, termios    # macOS / Linux
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    return "enter"
                if ch == "\x1b":
                    return "esc"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# 3. Look up a flashcard by acronym
def lookup_acronym(flashcards):
    """Find a card when the user already knows the acronym."""
    query = input("Type the acronym: ").strip()
    if not query:
        print("No acronym entered.")
        return
    
    query_upper = query.upper()
    matches = [
        card for card in flashcards
        if card["acronym"].strip().upper() == query_upper
    ]

    if not matches:
        print(f'No card found for "{query}".')
        return

    for card in matches:
        show_full_card(card)

# 4. Show a single flashcard with the option to reveal or go back to menu
def show_card(card, number=None, total=None):
    print("\n" + "=" * 50)
    if number is not None and total is not None:
        print(f"Card {number} of {total}")
    print(f"ACRONYM: {card['acronym']}")

    if overwrite_line("ENTER = reveal     ESC = menu") == "esc":
        return "esc"
    
    print(f"FULL NAME: {card['full_name']}")
    print(f"DESCRIPTION: {card['description']}")
    print("=" * 50)

    return overwrite_line("ENTER = next card     ESC = menu")

# 5. Show a full single flashcard without options
def show_full_card(card):
    """Show every field at once. No Enter/Esc options."""
    print("\n" + "=" * 50)
    print(f"ACRONYM:     {card['acronym']}")
    print(f"FULL NAME:   {card['full_name']}")
    print(f"DESCRIPTION: {card['description']}")
    print("=" * 50)
    input("Press ENTER to continue...")

# 6. Clear the hint line
def overwrite_line(text):
    """Print text, stay on the line, then erase it after the keypress."""
    print(text, end="", flush=True)
    action = read_enter_or_esc()
    print("\r" + " " * len(text) + "\r", end="", flush=True)
    return action

# 7. Main program loop
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
        print("3. Look up a specific acronym")
        print("4. Exit")
        
        choice = input("Enter 1, 2, 3, or 4: ").strip()
        
        if choice == "1":
            total = len(flashcards)
            for number, card in enumerate(flashcards, start=1):
                if show_card(card, number=number, total=total) == "esc":
                    break
                
        elif choice == "2":
            random.shuffle(flashcards)
            total = len(flashcards)
            for number, card in enumerate(flashcards, start=1):
                if show_card(card, number=number, total=total) == "esc":
                    break

        elif choice == "3":
            acronym = input("Enter the acronym you want to look up: ").strip().upper()
            found = False
            for card in flashcards:
                if card["acronym"].upper() == acronym:
                    show_full_card(card)    # full card, no key options
                    found = True
                    break
            if not found:
                print(f"No flashcard found for acronym: {acronym}")

        elif choice == "4":
            print()
            print("Thanks for studying! See you next time 👋")
            print("Made with ❤️ by TristanTango73")
            print("\n\n")
            break
        else:
            print("Invalid choice, please try again.")

# This runs the program when you type: python main.py
if __name__ == "__main__":
    main()