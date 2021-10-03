import requests
import sys
import json
from pathlib import Path

def get_pokemon(pokemon_id):
    req_data = {
        "url": f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}",
    }

    try:
        req = requests.get(**req_data)
        req.raise_for_status()
        if req.status_code == 200:
            return req.json()
    except Exception as e:
        print(e)
        print("Cound not get pokemon ", pokemon_id)


def save_pokemon(pokemon_info):
    file_name = f"{pokemon_info['id']}_{pokemon_info['name']}.json"
    with Path(f"examples/pokemons/{file_name}").open("w") as f:
        json.dump(pokemon_info, f, indent=4)

def get_pokemon_index(start=0, end=0):
    with Path("examples/pokemon-list.json").open("r") as f:
        return json.load(f)

def main():
    for pokemon in get_pokemon_index()["results"]:
        pok_info = get_pokemon(pokemon['url'].split("/")[-2])
        save_pokemon(pok_info)
    return 0


if __name__ == "__main__":
    sys.exit(main())