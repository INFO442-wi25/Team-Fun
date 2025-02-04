from ingredient import Ingredient
from typing import List

class Recipe:
    def __init__(self, name: str, ingredients: List[Ingredient], instructions: str, image_path: str):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.image_path = image_path
    
    def __repr__(self):
        return f"{self.name}"
