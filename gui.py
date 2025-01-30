import tkinter as tk
from tkinter import messagebox, simpledialog
from recipe_manager import RecipeManager




class RecipeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Manager")
        self.manager = RecipeManager()

        # Sample Data
        #self.manager.add_recipe("p", ["Flour", "Milk"], "Mix and cook.", "pancakes.jpg")

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        
        tk.Label(self.root, text="Recipe Manager", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="View Ingredients", command=self.show_ingredients).pack(pady=5)
        tk.Button(self.root, text="View Recipes", command=self.show_recipes).pack(pady=5)
        tk.Button(self.root, text="Add Ingredient", command=self.add_ingredient).pack(pady=5)
        tk.Button(self.root, text="Add Recipe", command=self.add_recipe).pack(pady=5)
        tk.Button(self.root, text="Use Recipe", command=self.use_recipe).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)


    def show_ingredients(self):
        self.clear_window()
        tk.Label(self.root, text="Ingredients List", font=("Arial", 14, "bold")).pack(pady=5)
        
        for ingredient in self.manager.list_ingredients():
            tk.Label(self.root, text=str(ingredient)).pack()
        
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def show_recipes(self):
        self.clear_window()
        tk.Label(self.root, text="Recipe List", font=("Arial", 14, "bold")).pack(pady=5)
        
        for recipe in self.manager.list_recipes():
            tk.Label(self.root, text=str(recipe)).pack()
        
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def add_ingredient(self):
        name = simpledialog.askstring("Ingredient Name", "Enter ingredient name:")
        #group = simpledialog.askstring("Ingredient Group", "Enter ingredient group (e.g., Dairy, Vegetable):")
        #storage = simpledialog.askstring("Storage", "Enter storage location (e.g., Fridge, Pantry):")

        if name:
            self.manager.add_ingredient(name, "group", "storage")
            messagebox.showinfo("Success", f"Added {name} to ingredients!")
        self.create_main_menu()

    def add_recipe(self):
        name = simpledialog.askstring("Recipe Name", "Enter recipe name:")
        ingredient_names = simpledialog.askstring("Ingredients", "Enter ingredients (comma separated):")
        instructions = simpledialog.askstring("Instructions", "Enter recipe instructions:")
        image_path = simpledialog.askstring("Image Path", "Enter image file path (optional):")

        if name and ingredient_names and instructions:
            ingredient_list = [i.strip() for i in ingredient_names.split(",")]
            self.manager.add_recipe(name, ingredient_list, instructions, image_path)
            messagebox.showinfo("Success", f"Added recipe: {name}")
        self.create_main_menu()

    def use_recipe(self):
        name = simpledialog.askstring("Use Recipe", "Enter recipe name:")
        if name:
            ingredients = self.manager.use_recipe(name)
            if ingredients:
                depleted = []
                for ing in ingredients:
                    if messagebox.askyesno("Depleted?", f"Did you use up {ing}?"):
                        depleted.append(ing)
                
                # Remove depleted ingredients
                for ing in depleted:
                    self.manager.remove_ingredient(ing.name)
                
                #messagebox.showinfo("Updated", f"Removed depleted ingredients: {', '.join(depleted)}")
                self.show_ingredients()
            else:
                messagebox.showerror("Error", "Recipe not found!")
        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = RecipeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
