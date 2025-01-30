class Ingredient:
    def __init__(self, name: str, group: str, storage: str):
        self.name = name
        self.group = group
        self.storage = storage
    
    def __repr__(self):
        return f"{self.name} ({self.group}, {self.storage})"
