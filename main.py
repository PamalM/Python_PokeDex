# main.py, Please execute this script to run the Pokedex.

import requests
import json
import os
from texttable import Texttable

# Function handles API Request and fetches information for the specified Pokemon.
def api_Request(pokemon):
    # Url to make API request. (Insert pokemon name, or id # at the end of url)
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower()
    evolutions_Url = '/evolution-chain/{param1}/'

    # Data directory will hold .json data locally for each searched pokemon.
    data_Path = 'DATA/' + pokemon.upper()

    # Create .json file for specific pokemon if it doesn't already exists.
    # No need to make API request if we have local Pokemon data available.
    try:
        # Create target Directory
        os.mkdir(data_Path)
        print('[{%s} DIRECTORY CREATED.]' % pokemon.upper())

        # Make API request.
        page = requests.get(url)
        print("[API Response: %s]" % page.status_code)

        # Convert to Python .json object.
        src = page.json()

        # Write json to local file in DATA directory.
        file = open(data_Path + "/" + pokemon.upper(), "w+")
        file.write(json.dumps(src))
        file.close()

    # Otherwise the directory already has information stored for this pokemon; No API request necessary.
    except FileExistsError:
        print('[{%s} DIRECTORY ALREADY EXISTS.]' % pokemon.upper())

def read_JSON(pokemon):
    # Open and load json file for reading.
    file =  open(('DATA/' + pokemon.upper() + "/" + pokemon.upper()))
    data = json.load(file)

    # Extract Pokemon name and Pokedex Id from API data.
    id = data['id']
    name = data['name']

    # Extract the type(s). Pokemon could either have 1 Type, or 2.
    type1 = data['types'][0]['type']['name']
    type2 = data['types'][1]['type']['name'] if len(data['types']) == 2 else 0
    types = [type1, type2] if len(data['types']) == 2 else [type1]

    # Extract the relevant stats for this pokemon.
    stats = data['stats']
    speed = stats[0]['base_stat']
    spDefence = stats[1]['base_stat']
    spAttack = stats[2]['base_stat']
    defence = stats[3]['base_stat']
    attack = stats[4]['base_stat']
    hp = stats[5]['base_stat']
    totalStats = speed + spDefence + spAttack + defence + attack + hp

    # Height and Weight for Pokemon; Convert API data to lbs and metres.
    weight = data['weight'] * 0.220462
    height = data['height'] * 0.1

    # Link to the image for this pokemon.
    image = data['sprites']['front_default']

    # Create and display table containing information relating to that particular pokemon.
    table = Texttable()
    table.add_row(['ID', 'NAME', 'TYPE(S)', 'HP', 'ATK', 'DEF', 'SP. ATK', 'SP. DEF', 'SPD',
                   'HEIGHT \n(m)', 'WEIGHT \n(lbs)', 'TOTAL'])
    table.add_row([id, name.upper(), str(types)[1:-1].upper().replace("'", ''), hp, attack, defence, spAttack, spDefence, speed,
                   height, weight, totalStats])
    table.set_cols_width([4, 15, 20, 4, 4, 4, 4, 4, 4, 6, 8, 6])
    print(table.draw())

    # Put all statistics into one list to reduce amount of parameters.
    statistics = [hp, attack, defence, spAttack, spDefence, speed]

    values = {'id': id, 'name': name.upper(), 'attack': attack, 'defence': defence, 'spAttack': spAttack, 'spDefence': spDefence,
              'speed': speed, 'height': height, 'weight': weight, 'totalStats': totalStats}

    # Return dictionary containing all relevant information of interest from json.
    return values


# api_Request('Charmander')
data = read_JSON('charmander')




