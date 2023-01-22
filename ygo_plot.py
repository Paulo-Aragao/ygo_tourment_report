# -*- coding: utf-8 -*-
"""YugiohGraph.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i9Rp-PpkspIPlG7rDdt9V3iUvYVETAkI
"""

#yugioh
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import json
import pandas as pd
from pickle import TRUE
import cv2 as cv
import matplotlib.image as mpimg
import math
import requests
from flask import Flask, render_template
from PIL import Image
import base64
import io

def read_image_url(url):
  resp = requests.get(url, stream=True).raw
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv.imdecode(image, cv.IMREAD_LOAD_GDAL)
  imageRGB = cv.cvtColor(image , cv.COLOR_BGR2RGB)
  return imageRGB

def img_to_pie( url, wedge, xy, zoom=1, ax = None):
    if ax==None: ax=plt.gca()
    user_agent = {"User-Agent": "Mozilla/5.0"}
    im = read_image_url(url)
    path = wedge.get_path()
    patch = PathPatch(path, facecolor='none')
    ax.add_patch(patch)
    imagebox = OffsetImage(im, zoom=zoom, clip_path=patch, zorder=-10)
    ab = AnnotationBbox(imagebox, xy, xycoords='data', pad=0, frameon=False)
    ax.add_artist(ab)

def apply_images(wedges,images,positions,zoom):
    for i in range(len(images)):
        url = images[i]
        img_to_pie(url, wedges[i], xy=positions[i], zoom= zoom[i] )
        wedges[i].set_zorder(5)

def create_positions(labels):
    positions = []
    for i in labels:
        positions.append((0,-0.5))
    return positions

def sort_arrays(images, names ,totals):
    num = totals
    totals,images = zip(*sorted(zip(num,images)))
    totals,names = zip(*sorted(zip(num,names)))
    return images, names ,totals

class deck_info():
    name : str
    key_card : str
    total : int
    top : int
    player : str
    def __init__(self,name,key_card ,total,top = False,player = None):
        self.name = name + " x"+str(total)
        self.image = self.get_image_of_card(key_card)[0]
        self.total = total
        self.top = top
        self.player = player
    def get_image_of_card(self,card_name):
        card_name = card_name.lower()
        return df_cards.loc[df_cards['name'] == card_name]["image_cropped"].values

def apply_zoom(total,totals):
    num_decks = sum(totals)
    factor = 2
    if num_decks < 8:
        factor = 1 + (num_decks/10) + 0.1
    if total == 1:
        return 0.36/factor
    elif total == 2:
        return 0.44/factor
    elif total >= 3:
        return 0.66/factor

def define_zoom_and_angles(totals,names):
    angle_per_slice = 360/sum(totals)
    i_slice = 0
    k = 0.5
    positions = []
    zooms = []
    for i in range(len(totals)):
        i_slice = i_slice+totals[i]
        res = ((i_slice * angle_per_slice) + 90) - (angle_per_slice * (totals[i]/2))
        print(names[i]+" -> "+str(res))
        positions.append((math.cos(math.radians(res)) * k,math.sin(math.radians(res)) * k))
        zooms.append(apply_zoom(totals[i],totals))
    return positions,zooms
def define_champion(decks):
    for deck in decks:
        if deck.top == 1:
            return deck.player,deck.name 
def plot_graphic(names,images,totals,positions,zooms,title,decks):
    fig = plt.figure()
    fig.patch.set_facecolor((0.1,0.2,0.2))
    champ,deck_c = define_champion(decks)
    plt.title(("campeão : " + champ+"({})".format(deck_c[:-3])).upper(),fontsize=14,color="green")
    plt.suptitle((title[:-4]+" "+str(sum(totals))+" jogadores").upper(),fontsize=18, y=1,color="white")
    plt.gca().axis("equal")

    wedges, texts = plt.pie(totals, startangle=90, labels=names,
                            wedgeprops = { 'linewidth': 2, "edgecolor" :"black","fill":False, 'linestyle': 'dashed'})
    
    apply_images(wedges,images,positions,zooms)
    i = 0
    for text in texts:
        if decks[i].top == 0: 
            text.set_color('gold')
        else:
            text.set_color('w')
        i += 1

    plt.savefig(title[:-4]+".png", dpi=300)
    #plt.show()

def get_image(decks,title):    
    
    decks.sort(key=lambda x: x.total, reverse=False)

    #lists
    images,names,totals = [],[],[]
    images,names,totals = [x.image for x in decks], [x.name for x in decks], [x.total for x in decks]
    positions,zooms= define_zoom_and_angles(totals,names)

    plot_graphic(names,images,totals,positions,zooms,title,decks)
     
def add_deck(deck_name,key_card,total,top = False,player = None):
    decks.append(deck_info(deck_name,key_card,total,top,player))

#flask

#app = Flask(__name__)


#setup
'''decks.append(deck_info("swordsoul","swordsoul of mo ye",1))
decks.append(deck_info("tearlaments","tearlaments rulkallos",4))
decks.append(deck_info("naturia","naturia sacred tree",1))
decks.append(deck_info("spright","spright blue",3))
decks.append(deck_info("dragon link","striker dragon",1))
decks.append(deck_info("subterror kashtira","subterror guru",1))
decks.append(deck_info("eldlich zombie","eldlich the golden lord",1))
decks.append(deck_info("floowandereeze","floowandereeze & empen",1))'''
'''
decks.append(deck_info("floowandereeze","floowandereeze & empen",2))
decks.append(deck_info("swordsoul","swordsoul of mo ye",1))
decks.append(deck_info("invoked","aleister the invoker",1))
decks.append(deck_info("spright","spright blue",1))
decks.append(deck_info("naturia","naturia sacred tree",2))
'''
'''decks.append(deck_info("swordsoul","swordsoul of mo ye",1))
decks.append(deck_info("tearlaments","tearlaments rulkallos",6))
decks.append(deck_info("naturia","naturia sacred tree",1))
decks.append(deck_info("spright","spright blue",3))
decks.append(deck_info("dragon link","striker dragon",1))
decks.append(deck_info("floowandereeze","floowandereeze & empen",1))
decks.append(deck_info("salamangreat","salamangreat gazelle",1))    
decks.append(deck_info("dinosaur","babycerasaurus",1))    
decks.append(deck_info("branded bystial","branded fusion",1))    
decks.append(deck_info("thunder dragon","thunder dragon",1))    
decks.append(deck_info("burning abyss","dante, traveler of the burning abyss",1))    
decks.append(deck_info("altergeist","altergeist multifaker",1))    
decks.append(deck_info("invoked branded","aleister the invoker",1))    
decks.append(deck_info("scareclaw ","scareclaw tri-heart",1))    '''

#variables
df_cards = pd.read_csv('https://drive.google.com/u/0/uc?id=1Bv1vFnb6ogY6-Atwguvb-dulwgtST4bK&export=download')
df_cards = df_cards[["name","image_cropped"]]
file_name = input("file name : ")
top_count = int(input('top cut : '))
df_tourment = pd.read_csv(file_name)
decks = []
unique_decks = []
unique_decks_names = []
for index, row in df_tourment.iterrows():
    deck = row["deck"]
    if deck not in unique_decks_names:
        unique_decks_names.append(deck)
        unique_decks.append((deck,row["image card"],1,row["posição"],row["jogador"]))
    else:
        unique_decks[unique_decks_names.index(deck)] = (unique_decks[unique_decks_names.index(deck)][0],
                                                        unique_decks[unique_decks_names.index(deck)][1],
                                                        unique_decks[unique_decks_names.index(deck)][2] + 1,
                                                        unique_decks[unique_decks_names.index(deck)][3],
                                                        unique_decks[unique_decks_names.index(deck)][4])

for deck in unique_decks:
    add_deck(deck[0],deck[1],deck[2],top=deck[3],player=deck[4])


get_image(decks,file_name)
decks = []
unique_decks = []
unique_decks_names = []
for index, row in df_tourment.iterrows():
    deck = row["deck"]
    if row["posição"] > top_count:
        continue
    if deck not in unique_decks_names:
        unique_decks_names.append(deck)
        unique_decks.append((deck,row["image card"],1,row["posição"],row["jogador"]))
    else:
        unique_decks[unique_decks_names.index(deck)] = (unique_decks[unique_decks_names.index(deck)][0],
                                                        unique_decks[unique_decks_names.index(deck)][1],
                                                        unique_decks[unique_decks_names.index(deck)][2] + 1,
                                                        unique_decks[unique_decks_names.index(deck)][3],
                                                        unique_decks[unique_decks_names.index(deck)][4])
for deck in unique_decks:
    add_deck(deck[0],deck[1],deck[2],top=deck[3],player=deck[4])

get_image(decks,"TOP "+file_name)

'''@app.route('/')
def home():
    #get_image()
    im = Image.open("histogram_img.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("home.html", img_data=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
    app.run()
'''


