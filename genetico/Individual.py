from typing import List
from Item import *
from constants import *

class Individual:
    def __init__(self, bits: List[int], items: List[Item]):
        self.bits = bits
        self.items = items
    
    def __str__(self):
        total_weight = sum([
            bit * item.weight
            for item, bit in zip(self.items, self.bits)
        ])
        return f"{self.bits} (Peso Mochila: {total_weight})"    

    def __hash__(self):
        return hash(str(self.bits))
    
    def fitness(self) -> float:
        total_value = sum([
            bit * item.value
            for item, bit in zip(self.items, self.bits)
        ])

        total_weight = sum([
            bit * item.weight
            for item, bit in zip(self.items, self.bits)
        ])

        if total_weight <= MAX_WEIGHT:
            return total_value
        
        return 0