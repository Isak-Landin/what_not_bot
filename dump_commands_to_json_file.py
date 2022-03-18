import json
from pathlib import Path

print(str(Path().resolve()))

commands_dict = {
    'commands':
        {
            "!rng": "You have boosted RNG NAME",
            "!test": 'Test response'
        }
}

with open(str(Path().resolve()) + r'\core\commands.json', 'w+') as file:
    json.dump(commands_dict, file, indent=4)