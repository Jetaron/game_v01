from api_client import APIClient
from game import Game
from character import Character
import time
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_character(character: Character) -> None:
    """Display character information"""
    print(f"\n{character.name}:")
    print(f"HP: {character.health:.1f}/{character.max_health}")
    print(f"DMG: {character.damage}")
    print(f"ARM: {character.armor}")
    print(f"RES: {character.resist*100}%")
    print(f"SPD: {character.speed}")

def main():
    # Initialize game
    print("Initializing game...")
    game = Game()

    # Load characters from API
    api = APIClient("https://genshin.jmp.blue")
    try:
        characters = api.load_characters(limit=3)  # Load 3 characters
        for char in characters:
            game.add_character(char)
    except Exception as e:
        print(f"Error loading characters: {str(e)}")
        return

    # Main game loop
    while not game.is_game_over():
        clear_screen()
        
        # Display character status
        print("\n=== Character Status ===")
        for char in game.characters:
            display_character(char)

        # Execute turn
        print("\n=== Turn Events ===")
        events = game.execute_turn()
        for event in events:
            print(event)
            time.sleep(1)  # Add dramatic pause

        # Save game after each turn
        try:
            game.save_game("savegame.pkl")
        except Exception as e:
            print(f"Failed to save game: {str(e)}")

        input("\nPress Enter for next turn...")

    # Game Over
    clear_screen()
    print("\n=== Game Over ===")
    winner = game.get_winner()
    if winner:
        print(f"\nWinner: {winner.name}!")
    
    print("\nBattle History:")
    for event in game.turn_history:
        print(event)

if __name__ == "__main__":
    main()
