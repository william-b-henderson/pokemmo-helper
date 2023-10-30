import json

from Levenshtein import distance as levenshtein_distance

from screen_reader import get_text


def find_closest_word(search_string: str, data: dict):
    """
    Finds the key that is the closest to the search_string.
    """
    closest_match = min(
        data.keys(), key=lambda word: levenshtein_distance(search_string, word))
    print(f"Closest match for '{search_string}' is '{closest_match}'")
    return closest_match


def print_route_pokemon(route_dict: dict):
    for location in route_dict:
        print(location)
        for pokemon in route_dict[location]:
            pokemon_name = pokemon["pokemon_name"]
            rarity = pokemon["rarity"]
            items = pokemon["items"]
            horde = pokemon["horde"]
            time = pokemon["time"]
            print(
                f"Pokemon: {pokemon_name} ({rarity}) {'(Horde)' if horde else ''} {time if time else ''} {f'[{items}]' if items else ''}")


if __name__ == "__main__":
    with open("route_data.json", 'r') as f:
        data = json.load(f)
    text, _, _ = get_text()
    if text is None:
        print("Error getting text from image")
        exit
    closest_word = find_closest_word(search_string=text, data=data)
    print_route_pokemon(data[closest_word])
