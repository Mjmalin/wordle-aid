import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import sys

lst = list()
greylist = list()
yellowlist = list()
greenlist = list()
counts = dict()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# import all possible Wordle solutions into a list
html = urllib.request.urlopen("https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/45c977427419a1e0edee8fd395af1e0a4966273b/wordle-answers-alphabetical.txt", context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
for lines in soup :
    x = lines.rstrip()
    y = x.split()
    for z in y :
        lst.append(z)

# import all past Wordle answers
html = urllib.request.urlopen("https://www.rockpapershotgun.com/wordle-past-answers", context=ctx).read()
sp = BeautifulSoup(html, 'html.parser')

words = sp.find_all("ul", class_="inline")
a = re.findall("<li>([A-Z]+)", str(words))
c = [b.lower() for b in a]

# subtract all past Wordle answers from all possible Wordle solutions
l3 = [d for d in lst if d not in c]
print(l3)

# continue asking for Wordle entries unless there is one word left
while True:
    if len(l3) < 2:
        sys.exit()
        
    # count letters and print amount of each
    for remaining in l3:
        for letters in remaining:
            counts[letters] = counts.get(letters, 0) + 1
    for letters, count in sorted(counts.items(), key=lambda k: k[1], reverse=True):
        print(letters, count)
        
    # ask for green letters
    while True:
        green = input("Enter a green letter: ")
        if green == "":
            break
        if green == "exit":
            sys.exit()
        greenlist.append(green)
        print(greenlist)

    # ask for positions, subtract words with no green letters in that position
        gpos = input("Enter position: ")
        gp = int(gpos)
        gpi = gp - 1
        l3 = [j for j in l3 if j[gpi] == green]
    print(l3)
        
    # ask for yellow letters
    while True:
        yellow = input("Enter a yellow letter: ")
        if yellow == "":
            break
        if yellow == "exit":
            sys.exit()
        yellowlist.append(yellow)
        print(yellowlist)

    # ask for positions, subtract words with yellow letters in that position
        ypos = input("Enter position: ")
        yp = int(ypos)
        ypi = yp - 1
        l3 = [g for g in l3 if g[ypi] != yellow]

    # subtract words with none of the yellow letters 
    l3 = [h for h in l3 if all(i in h for i in yellowlist)]
    print(l3)
    
    # ask for grey letters, subtract all words with grey letters
    while True:
        grey = input("Enter a grey letter: ")
        if grey == "":      
            break  
        if grey == "exit":
            sys.exit()
        # don't add letter to greylist if in yellowlist or greenlist
        
        greylist.append(grey)
    print(greylist)
    l3 = [e for e in l3 if all(f not in e for f in greylist)]
    print(l3)

    # prepare for next Wordle entry
    counts.clear()
    greenlist.clear()
    yellowlist.clear()
    greylist.clear()