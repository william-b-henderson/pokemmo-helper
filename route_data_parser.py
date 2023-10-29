import json
import re

data = {}  # Initialize the data dictionary
current_route = ""
current_condition = ""

def contains_colon(line):
  return contains_character(line, ":")

def contains_star(line):
  return contains_character(line, "*")

def contains_character(line, char):
  return line.find(char) != -1

def clean_pokemon_name(name: str):
  name = name.strip()
  if name.find("png") == 0:
    return name[3:]
  if name.find("and ") != -1:
    return name[4:]
  return name

def parse_route(route: str):
  if route.find("(no encounters)") != -1:
    loc = route.find("(no encounters)")
    return route[:loc].strip()
  return route.strip()

with open('unova_raw_route_data.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            if not contains_character(line, ":") and not contains_character(line, "*"):
                current_route = line
                current_route = parse_route(current_route)
                data[current_route] = {}
            elif current_route:
                if contains_character(line, ":"):
                    parts = re.split(r':', line, 1)
                    current_condition = parts[0]
                    data[current_route][current_condition] = []
                    content = parts[1].strip()
                    if content:
                            # Define a regex pattern to match the fields
                            pattern = r'([\w\s-]+) \(([^)]+)\)(?: \[(?:Item: ([^]]+))\])?(?: \(([^)]+)\))?(?: \*Horde)?'

                            # Initialize the results list to store extracted data
                            results = []

                            # Find all matches in the text
                            matches = re.findall(pattern, content)

                            # Process each match and populate the results
                            for match in matches:
                                pokemon_name = clean_pokemon_name(match[0])
                                rarity = match[1]
                                items = match[2] if match[2] else False
                                time = match[3] if match[3] else False
                                horde = False
                                if rarity:
                                  if rarity.find("Horde") != -1:
                                    rarity = rarity[:rarity.find("Horde") - 2]
                                    horde = True

                                results.append({
                                    'pokemon_name': pokemon_name,
                                    'rarity': rarity,
                                    'horde': horde,
                                    'time': time,
                                    'items': items
                                })
                            data[current_route][current_condition] = results


# Save the data as JSON
with open('route_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data saved to 'route_data.json'")
