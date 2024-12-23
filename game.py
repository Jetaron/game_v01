from typing import List, Optional
from character import Character
import json
import pickle
from datetime import datetime

class Game:
    def __init__(self):
        self.characters: List[Character] = []
        self.turn_history: List[str] = []
        self.current_turn: int = 0

    def add_character(self, character: Character) -> None:
        """Add a character to the game"""
        self.characters.append(character)

    def get_living_characters(self) -> List[Character]:
        """Get list of characters that are still alive"""
        return [char for char in self.characters if char.is_alive()]

    def is_game_over(self) -> bool:
        """Check if game is over (0 or 1 character remaining)"""
        return len(self.get_living_characters()) <= 1

    def execute_turn(self) -> List[str]:
        """Execute a single turn of the game"""
        if self.is_game_over():
            return ["Game is over!"]

        turn_events = []
        living_chars = self.get_living_characters()
        
        # Sort by speed
        living_chars.sort(key=lambda x: x.speed, reverse=True)

        for attacker in living_chars:
            if not attacker.is_alive():
                continue

            # Find first living character that isn't the attacker
            targets = [c for c in living_chars if c != attacker and c.is_alive()]
            if not targets:
                break

            target = targets[0]  # Simple AI: attack first available target
            damage = attacker.attack(target)
            
            event = f"Turn {self.current_turn}: {attacker.name} attacks {target.name} for {damage} damage! "
            event += f"({target.name} HP: {target.health:.1f}/{target.max_health})"
            
            turn_events.append(event)
            
            if not target.is_alive():
                turn_events.append(f"{target.name} has been defeated!")

        self.turn_history.extend(turn_events)
        self.current_turn += 1
        return turn_events

    def save_game(self, filename: str) -> None:
        """Save game state to file"""
        with open(filename, 'wb') as f:
            pickle.dump({
                'characters': self.characters,
                'turn_history': self.turn_history,
                'current_turn': self.current_turn
            }, f)

    def load_game(self, filename: str) -> None:
        """Load game state from file"""
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.characters = data['characters']
            self.turn_history = data['turn_history']
            self.current_turn = data['current_turn']

    def get_winner(self) -> Optional[Character]:
        """Get the winning character if game is over"""
        living = self.get_living_characters()
        return living[0] if len(living) == 1 else None
