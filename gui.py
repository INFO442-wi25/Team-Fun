import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from recipe_manager import RecipeManager

class RecipeGUI:
    def __init__(self, root):
        self.root = root  # Enable drag and drop
        self.root.title("Recipe Manager")
        self.manager = RecipeManager()
        self.image_path = ""  # Store the image path after drag and drop

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
        self.clear_window()
        tk.Label(self.root, text="Add Recipe", font=("Arial", 14, "bold")).pack(pady=10)
        
        name = simpledialog.askstring("Recipe Name", "Enter recipe name:")
        ingredient_names = simpledialog.askstring("Ingredients", "Enter ingredients (comma separated):")
        instructions = simpledialog.askstring("Instructions", "Enter recipe instructions:")
        
        if name and ingredient_names and instructions:
            self.image_path = ""  # Reset image path before drag-and-drop
            self.create_drag_and_drop_widget(name, ingredient_names, instructions)
        else:
            messagebox.showerror("Error", "All fields except image are required.")
            self.create_main_menu()

        print(name + ingredient_names + instructions + self.image_path)

    def create_drag_and_drop_widget(self, name, ingredient_names, instructions):
        tk.Label(self.root, text="Drop an image file here (optional)", bg="lightgray", fg="black", relief="ridge", width=50, height=5).pack(pady=20)
        file_label = tk.Label(self.root, text="Drop a file here", bg="lightgray", fg="black", relief="ridge", width=50, height=5)
        file_label.pack(pady=10)
        
        file_label.drop_target_register(DND_FILES)
        file_label.dnd_bind('<<Drop>>', lambda event: self.drop(event, file_label, name, ingredient_names, instructions))
        
        tk.Button(self.root, text="Submit Recipe", command=lambda: self.save_recipe(name, ingredient_names, instructions)).pack(pady=10)
        tk.Button(self.root, text="Cancel", command=self.create_main_menu).pack(pady=5)

    def drop(self, event, file_label, name, ingredient_names, instructions):
        self.image_path = event.data.strip()
        file_label.config(text=self.image_path)
        with open("file_paths.txt", "a") as f:
            f.write(self.image_path + "\n")

    def save_recipe(self, name, ingredient_names, instructions):
        ingredient_list = [i.strip() for i in ingredient_names.split(",")]
        self.manager.add_recipe(name, ingredient_list, instructions, self.image_path if self.image_path else None)
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
    root = TkinterDnD.Tk()
    app = RecipeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

