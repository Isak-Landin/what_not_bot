import json
from pathlib import Path

print(str(Path().resolve()))

commands_dict = {
    'greetings': ["it's great seeing you here!", "what a pleasure seeing you here!",
               "welcome to the stream of opportunity!", "days and nights pass and finally you are here"]
}

with open(str(Path().resolve()) + r'\core\greetings.json', 'w+') as file:
    json.dump(commands_dict, file, indent=4)