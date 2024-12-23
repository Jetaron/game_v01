from dataclasses import dataclass
from typing import Optional

@dataclass
class Character:
    name: str
    health: float
    damage: float
    armor: float
    resist: float
    speed: float = 1.0
    max_health: Optional[float] = None

    def __post_init__(self):
        if self.max_health is None:
            self.max_health = self.health

    def is_alive(self) -> bool:
        return self.health > 0

    def calculate_damage(self, target: 'Character') -> float:
        """Calculate damage against target using the formula: final_damage = max(0, damage - armor) * (1 - resist)"""
        raw_damage = max(0, self.damage - target.armor)
        final_damage = raw_damage * (1 - target.resist)
        return round(final_damage, 2)

    def attack(self, target: 'Character') -> float:
        """Attack target and return damage dealt"""
        if not self.is_alive():
            return 0
        
        damage = self.calculate_damage(target)
        target.health = max(0, target.health - damage)
        return damage

    def heal(self, amount: float) -> float:
        """Heal character and return amount healed"""
        if not self.is_alive():
            return 0
            
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before
