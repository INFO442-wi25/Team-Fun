import json
from ingredient import Ingredient
from recipe import Recipe
from typing import List, Dict

class RecipeManager:
    def __init__(self):
        self.ingredients: Dict[str, Ingredient] = {}
        self.recipes: Dict[str, Recipe] = {}
        self.load_ingredients()  # Load ingredients from JSON on startup

    def add_ingredient(self, name: str, group: str, storage: str):
        ingredient = Ingredient(name, group, storage)
        self.ingredients[name] = ingredient
        self.save_ingredients()  # Save to JSON after adding

    def list_ingredients(self):
        return list(self.ingredients.values())

    def save_ingredients(self):
        """Save ingredients to ingredients.json."""
        with open("ingredients.json", "w") as file:
            json.dump(
                {name: {"group": ing.group, "storage": ing.storage} for name, ing in self.ingredients.items()},
                file,
                indent=4
            )

    def remove_ingredient(self, name: str):
        if name in self.ingredients:
            del self.ingredients[name]
            self.save_ingredients()


    def load_ingredients(self):
        """Load ingredients from ingredients.json."""
        try:
            with open("ingredients.json", "r") as file:
                data = json.load(file)
                for name, details in data.items():
                    self.ingredients[name] = Ingredient(name, details["group"], details["storage"])
        except (FileNotFoundError, json.JSONDecodeError):
            self.ingredients = {}  # Default to empty if file is missing/corrupt
    
    def add_recipe(self, name: str, ingredient_names: List[str], instructions: str, image_path: str):
        ingredients = [self.ingredients[ing] for ing in ingredient_names if ing in self.ingredients]
        self.recipes[name] = Recipe(name, ingredients, instructions, image_path)
    
    def list_recipes(self):
        return list(self.recipes.values())

    def use_recipe(self, recipe_name: str):
        if recipe_name in self.recipes:
            return self.recipes[recipe_name].ingredients
        return None
