import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from recipe_manager import RecipeManager
import csv
from PIL import Image, ImageTk

class RecipeGUI:
    def __init__(self, root):
        self.root = root  # Enable drag and drop
        self.root.title("Recipe Manager")
        self.manager = RecipeManager()
        self.image_path = ""  # Store the image path after drag and drop
        self.ingredients_list = self.load_ingredients_from_csv()
        self.create_main_menu()

    def load_ingredients_from_csv(self):
        ingredients = []
        with open("Ingredient.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                ingredients.append(row[1])  # Assuming the first column is the ingredient name
        return ingredients    
    
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
        
        for recipe_name in self.manager.list_recipes():
            label = tk.Label(self.root, text=str(recipe_name), fg="blue", cursor="hand2")
            label.pack()

            def on_click(event, name=recipe_name):
                self.open_recipe_window(name)

            label.bind("<Button-1>", on_click)  # Bind left-click event to recipe label

        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)


    def open_recipe_window(self, recipe):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Recipe: {recipe}")

        tk.Label(new_window, text=f"{recipe}", font=("Arial", 14, "bold")).pack(pady=10)

        
        if recipe:
            tk.Label(new_window, text="Ingredients:", font=("Arial", 12, "bold")).pack(pady=5)
            for ingredient in recipe.ingredients:
                tk.Label(new_window, text=ingredient).pack()

            tk.Label(new_window, text="Instructions:", font=("Arial", 12, "bold")).pack(pady=5)
            tk.Label(new_window, text=recipe.instructions, wraplength=400).pack(pady=5)

            if recipe.image_path:
                try:
                    image = Image.open(recipe.image_path)
                    width = 600
                    w_percent = (width / float(image.size[0]))
                    height = int((float(image.size[1]) * float(w_percent)))
                    image = image.resize((width, height))
                    photo = ImageTk.PhotoImage(image)
                    tk.Label(new_window, image=photo).pack(pady=10)
                    new_window.image = photo  # Keep a reference to avoid garbage collection
                except Exception as e:
                    tk.Label(new_window, text=f"Error loading image: {e}").pack(pady=5)
        else:
            tk.Label(new_window, text="Recipe not found.", font=("Arial", 12, "bold")).pack(pady=10)

    def add_ingredient(self):
        self.clear_window()
        tk.Label(self.root, text="Add Ingredient", font=("Arial", 14, "bold")).pack(pady=10)

        ingredient_var = tk.StringVar()
        combobox = ttk.Combobox(self.root, textvariable=ingredient_var)
        combobox.pack(pady=10)

        def update_combobox(*args):
            search_term = ingredient_var.get()
            filtered_list = [ingredient for ingredient in self.ingredients_list if ingredient.lower().startswith(search_term.lower())]
            combobox['values'] = filtered_list

        ingredient_var.trace("w", update_combobox)

        def on_select(event):
            name = combobox.get()
            if name:
                self.manager.add_ingredient(name, "group", "storage")
                messagebox.showinfo("Success", f"Added {name} to ingredients!")
                self.create_main_menu()

        combobox.bind("<<ComboboxSelected>>", on_select)

        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

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
        self.clear_window()
        tk.Label(self.root, text="Use Recipe", font=("Arial", 14, "bold")).pack(pady=10)

        recipe_var = tk.StringVar()
        combobox = ttk.Combobox(self.root, textvariable=recipe_var)
        combobox.pack(pady=10)

        def update_combobox(*args):
            search_term = recipe_var.get()
            filtered_list = [recipe for recipe in self.manager.list_recipes() if recipe.name.lower().startswith(search_term.lower())]
            combobox['values'] = filtered_list

        recipe_var.trace("w", update_combobox)

        def on_select(event):
            name = combobox.get()
            if name:
                self.manager.use_recipe(name)
                messagebox.showinfo("Success", f"Using recipe: {name}")
                self.create_main_menu()

        combobox.bind("<<ComboboxSelected>>", on_select)

        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = TkinterDnD.Tk()
    app = RecipeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

