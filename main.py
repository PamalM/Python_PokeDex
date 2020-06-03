# main.py, Please execute this script to run the Pokedex.

import requests
import json
import os
from texttable import Texttable
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


# Function performs the API request for information for the specified pokemon.
def fetch_JSON(pokemon):

    # url for pokeAPI database.
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower()

    # Perform API request and output the response code from the fetch.
    page = requests.get(url)
    response = page.status_code
    print("\n[API Response: %s]" % page.status_code)

    # Check for a valid response from the API.
    if response == 200:

        # Data directory will hold (.json) data locally for each searched pokemon.
        data_Path = 'DATA/' + pokemon.upper()

        try:
            # Convert to Python (.json) object.
            src = page.json()

            # Create directory for pokemon's stats.
            os.mkdir(data_Path)
            print('[{%s} DIRECTORY CREATED.]' % pokemon.upper())

            # Write (json) to file to be saved.
            file = open(data_Path + "/" + pokemon.upper(), "w+")
            file.write(json.dumps(src))
            file.close()

        # Information for this pokemon already exists in a local directory.
        except FileExistsError:
            print('[{%s} DIRECTORY ALREADY EXISTS.]' % pokemon.upper())

        return response

    # Bad request made (error in pokemon name or id).
    else:
        return response


# Read and return dictionary of stats for specified pokemon from json data file.
def read_JSON(pokemon):

    # Open and load json file for reading.
    file = open(('DATA/' + pokemon.upper() + "/" + pokemon.upper()))
    data = json.load(file)

    # Extract Pokemon name and Pokedex Id from API data.
    id = data['id']
    name = data['name']

    # Extract the type(s). Pokemon could either have 1-2 types.
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

    # Format height and weights decimal points (limit to 2 decimal places).
    weight_Format = "%.2f" % weight
    height_Format = "%.2f" % height

    values = {'id': id, 'name': name.upper(), 'type': types, 'hp': hp, 'attack': attack, 'defence': defence, 'spAttack': spAttack,
              'spDefence': spDefence, 'speed': speed, 'height': height_Format,
              'weight': weight_Format, 'totalStats': totalStats, 'imageUrl': image}

    # Return dictionary containing all relevant information of interest from json.
    return values


# Function creates GUI for user to search pokemon by their name or id.
def searchPokemon():

    # Function re-sizes background image to be same size on window resize.
    def resize_BG_master(event):
        new_width = master.winfo_width()
        new_height = master.winfo_height()
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        background.config(image=photo)
        # Avoid garbage collection.
        background.image = photo

    # Function transfers user to next screen to view pokemon stats.
    def submitSearch(pokemon):

        # Function draws a graph model to be displayed in the next GUI.
        def drawStats(array, total, name):

            # Formats the labels on the pie chart to a specific format.
            def autopct_format(values):
                def my_format(pct):
                    val = int(round(pct * total / 100.0))
                    return '{v:d}'.format(v=val)

                return my_format

            # Create a pie chart model to output as a png model on display GUI.
            labels = ['HP', 'ATK', 'DEF', 'SP. ATK', 'SP. DEF', 'SPD']
            colors = ['#49B537', '#17639E', '#D8481F', '#78B7E7', '#DB9A88', '#DEDC36']
            plt.pie(array, labels=labels, colors=colors,
                    autopct = autopct_format(array), startangle=90)

            plt.savefig('DATA/' + name + "/" + name + "_stats" + '.png')  # save the figure to file

        # Get response code from API.
        response = fetch_JSON(pokemon)

        # If the response was valid from the API (True = 200) then proceed to next GUI.
        if response == 200:
            data = read_JSON(pokemon)

            # Retrieve and download a image for this pokemon.
            img_Request = requests.get(data['imageUrl']).content
            with open('DATA/' + pokemon.upper() + "/" + pokemon.upper() + '.png', 'wb') as handler:
                handler.write(img_Request)

            # Generate the stats model that will be displayed in the next GUI.
            drawStats([data['hp'], data['attack'], data['defence'],
                       data['spAttack'], data['spDefence'], data['speed']], data['totalStats'], data['name'].upper())

            # Call function to display pokemon's attributes and statistics.
            displayPokemon(data)

        # This means that the response code was invalid (False = 404, etc). Display error screen.
        else:
            print(str(response) + " to be implemented")

    # Create tkinter window object.
    master = tk.Tk()

    # Create label for GUI background image.
    loadImage = Image.open("background.png")
    copy_of_image = loadImage.copy()
    background_image = ImageTk.PhotoImage(loadImage)
    background = tk.Label(master, image=background_image)
    background.pack()

    # Just some text labels. . .
    label1 = tk.Label(background, text='ENTER POKÉMON NAME:', background='black')
    label1.config(font='Helvetica 30 bold', fg='white')
    label1.pack(fill=tk.BOTH, padx=80, pady=(120, 10))

    # String variable to contain searched pokemon name/id from entry().
    search = tk.StringVar()

    # Search bar allows user to enter their search for id or name of a pokemon.
    searchBar = tk.Entry(background, textvariable=search, font="Helvetica 44 bold", justify="center")
    searchBar.pack(fill=tk.BOTH, padx=80, pady=14)

    # Search button directs user to next GUI.
    searchButton = tk.Button(background, text='SEARCH', font='Helvetica 40 bold')
    searchButton.config(highlightbackground='red', fg='white', command=lambda: submitSearch(search.get()))
    searchButton.pack(fill=tk.BOTH, padx=225)

    # Window attributes for tkinter object.
    master.title('Python Pokédex')
    master.geometry('750x500')
    master.bind('<Configure>', resize_BG_master)
    master.mainloop()


def displayPokemon(data):

    # Function re-sizes background image to be same size on window resize.
    def resize_BG_root(event):
        new_width = root.winfo_width()
        new_height = root.winfo_height()
        image = copy_of_Image_Display.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        background_Display.config(image=photo)
        # Avoid garbage collection.
        background_Display.image = photo

    root = tk.Toplevel()

    # Create label for GUI background image.
    loadImage_Display = Image.open("background_Display.png")
    copy_of_Image_Display = loadImage_Display.copy()
    background_Image_Display = ImageTk.PhotoImage(loadImage_Display)
    background_Display = tk.Label(root, image=background_Image_Display)
    background_Display.pack()

    # Label displays pokemon's image.
    loadImage_Pokemon = Image.open('DATA/' + data['name'].upper() + "/" + data['name'].upper() + '.png')
    copy_of_Image_ = loadImage_Pokemon.copy()
    image = loadImage_Pokemon.resize((150, 150), Image.ANTIALIAS)
    background_Image_ = ImageTk.PhotoImage(image)
    background_ = tk.Label(background_Display, image=background_Image_)
    background_.pack(pady=(55, 0))

    # Display additional information underneath.
    nameLabel = tk.Label(background_Display, text=" #" + str(data['id']) + "\n" + data['name'] + " ",
                         fg='white', bg='black', font='HELVETICA 20 bold')
    nameLabel.pack(side="top", fill="x", padx=80)

    if len(data['type']) == 2:
        typeLabel = tk.Label(background_Display, text=str(data['type'][0].upper() + ", " + data['type'][1].upper()),
                             fg='black', font='HELVETICA 18 bold')
        typeLabel.pack(pady=(4, 0))

    else:
        typeLabel = tk.Label(background_Display, text=str(data['type'][0].upper()), fg='black', font='HELVETICA 18 bold')
        typeLabel.pack(pady=(4, 0))

    hwLabel = tk.Label(background_Display, text=str(data['height']) + "(m)" + "  " + str(data['weight']) + '(lbs)',
                       font='HELVETICA 16 bold', fg='black')
    hwLabel.pack()

    hpLabel = tk.Label(background_Display, text='HP: ' + str(data['hp']), fg='green', font='HELVETICA 24 bold')
    hpLabel.pack(pady=(6, 0))

    atkLabel = tk.Label(background_Display, text='ATK: ' + str(data['attack']), fg='medium blue', font='HELVETICA 24 bold')
    atkLabel.pack(fill=tk.X)

    defLabel = tk.Label(background_Display, text='DEF: ' + str(data['defence']), fg='red4', font='HELVETICA 24 bold')
    defLabel.pack()

    spAtkLabel = tk.Label(background_Display, text='SP. ATK: ' + str(data['spAttack']), fg='slategray3', font='HELVETICA 24 bold')
    spAtkLabel.pack()

    spDefLabel = tk.Label(background_Display, text='SP. DEF: ' + str(data['spDefence']), fg='brown1', font='HELVETICA 24 bold')
    spDefLabel.pack()

    spdLabel = tk.Label(background_Display, text='SPD: ' + str(data['speed']), fg='magenta', font='HELVETICA 24 bold')
    spdLabel.pack()

    # Window attributes for root.
    root.title('Python Pokédex')
    root.geometry('400x700')
    root.minsize(400, 700)
    root.bind('<Configure>', resize_BG_root)
    root.mainloop()


print('[Python Pokédex booted up.]')
searchPokemon()