import json
from pathlib import Path


def get_accounts_data():
    path = Path()
    with open(str(path.resolve()) + r'\help_scripts\account_data.json', 'r') as file:
        data = json.load(file)

    password = data['Account']['password']
    secret_phrase = data['Account']['phrase']
    #
    return password, secret_phrase
