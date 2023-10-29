import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk

from screen_reader import get_text
from utils import find_closest_word

# Sample Pokemon data
pokemon_data = {
    "Grass": [
        {"pokemon_name": "Lillipup", "rarity": "Very Common",
            "horde": False, "time": False, "items": False},
        {"pokemon_name": "Patrat", "rarity": "Very Common",
            "horde": False, "time": False, "items": False}
    ],
    # Other locations and Pokemon data...
}


class PokeGUI():

    def __init__(self) -> None:
        with open("route_data.json", 'r') as f:
            self.data = json.load(f)
        self.route_name = None
        self.pokemon_data = None
        self.root = tk.Tk()
        self.displayed_data = []
        return
    # Function to create the GUI

    def create_gui(self):
        self.root.title("Pokemon Data")

        # Set the transparency of the window
        self.root.attributes("-alpha", 0.7)

        # Configure the window to be always on top
        self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        self.create_widgets()

        self.generate_pokemon_list()
        self.root.mainloop()

    def create_widgets(self):
        self.route_button = tk.Button(
            self.root, text="Get route", command=self.get_route)
        self.route_button.grid(row=0, column=0)
        self.clear_button = tk.Button(
            self.root, text='Clear', command=self.reset_gui)
        self.clear_button.grid(row=1, column=0)

        self.text = ScrolledText(self.root, wrap=tk.WORD, width=40)
        self.text.grid(row=2, column=0, padx=10, pady=10)

        self.text.pokemon = []
        self.text.images = []

    def reset_gui(self):
        self.text.delete('1.0', tk.END)
        self.text.pokemon.clear()
        self.text.images.clear()

    def get_route(self):
        text = get_text()
        self.route_name = find_closest_word(search_string=text, data=self.data)
        self.pokemon_data = self.data[self.route_name]
        self.generate_pokemon_list()
    # Function to set the label style based on rarity

    def set_label_style(self, rarity: str):
        if "Very Common" in rarity:
            return "gray"
        elif "Common" in rarity:
            return "black"
        elif "Uncommon" in rarity:
            return "green"
        elif "Shadow" in rarity:
            return "red"
        elif "Bubble - Fishing" in rarity:
            return "blue"
        else:
            return "black"

    def generate_pokemon_list(self):
        # Create labels for each location and its Pokemon data
        if self.pokemon_data is None:
            print("pokemon data is not defined.")
            return
        print("Loading pokemon into gui...")
        self.text.delete('1.0', tk.END)
        self.reset_gui()
        self.text.insert(tk.INSERT, self.route_name + '\n')
        for location, pokemons in self.pokemon_data.items():
            self.text.insert(tk.INSERT, location + '\n')
            for pokemon in pokemons:
                pokemon_info = f"{pokemon['pokemon_name']} - {pokemon['rarity']}"
                rarity_color = self.set_label_style(pokemon['rarity'])
                # Load image using PIL
                image_path = f"sprites/{pokemon['pokemon_name'].lower()}.png"
                try:
                    img = Image.open(image_path).resize((32, 32))
                    img = ImageTk.PhotoImage(img)
                    self.text.image_create(tk.INSERT, image=img)
                    self.text.images.append(img)
                except Exception as e:
                    print(
                        f'could not find image for {pokemon["pokemon_name"]}')
                self.text.insert(tk.INSERT, pokemon_info + '\n', rarity_color)
                self.text.tag_config(rarity_color, foreground=rarity_color)
                self.text.pokemon.append(pokemon_info)


if __name__ == "__main__":
    # Create the GUI
    gui = PokeGUI()
    gui.create_gui()
