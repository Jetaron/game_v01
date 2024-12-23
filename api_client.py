import requests
from typing import List, Dict, Any
import json
from character import Character

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def get_characters(self) -> List[str]:
        """Get list of available character names from API"""
        try:
            response = requests.get(f"{self.base_url}/characters")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch characters: {str(e)}")

    def get_character_details(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a specific character"""
        try:
            response = requests.get(f"{self.base_url}/characters/{name}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch character {name}: {str(e)}")

    def create_character(self, data: Dict[str, Any]) -> Character:
        """Create Character instance from API data"""
        # For demo purposes, we'll use some default values since the actual API
        # doesn't provide game-specific stats
        return Character(
            name=data.get('name', 'Unknown'),
            health=100,  # Default values since API doesn't provide game stats
            damage=20,
            armor=10,
            resist=0.1,
            speed=1.0
        )

    def load_characters(self, limit: int = 2) -> List[Character]:
        """Load multiple characters from API"""
        characters = []
        try:
            char_names = self.get_characters()
            for name in char_names[:limit]:  # Limit number of characters
                data = self.get_character_details(name)
                character = self.create_character(data)
                characters.append(character)
            return characters
        except Exception as e:
            raise Exception(f"Failed to load characters: {str(e)}")
