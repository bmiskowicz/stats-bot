# importing the libraries
from numpy import zeros
from bs4 import BeautifulSoup
import requests
import os
import re


def getData(name, team, link, url):
    #Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    #Parse the html content
    soup = BeautifulSoup(html_content, "lxml")

    #Get the table having the class 
    gdp_table = soup.find("table", attrs={"class": "rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive"})


    i=0
    a = zeros(18, float)

    for td in gdp_table.find_all("tr"):
        tekst = td.text
        tekst=tekst.split()
        #looking for stats from whole season
        if "Łącznie" in tekst:
            for xd in tekst:
                try:
                    xd = xd.replace(',','.') #changing comas to dots
                    a[i]=float(xd)
                    i=i+1
                except ValueError:
                    pass    

    #save stats to .txt file
    local_dir = os.path.dirname(__file__)
    with open(os.path.join(local_dir, "staty.txt"), "a") as file:
        data = ' '.join(str(e) for e in a)
        file.write(f'{data}\n') 


def getPlayers():
    #Make a GET request to fetch the raw HTML content
    htmlPlayers = requests.get("https://www.plusliga.pl/players.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D").text

    #Parse the html content
    soupPlayers = BeautifulSoup(htmlPlayers, "html.parser")

    #Get the table having the div 
    gdpPlayers = soupPlayers.find("div", id="hiddenPlayersListAllBuffer")

    #tables for players data
    names_table = []
    teams_table = []
    links_table = []
    positions_table = []

    
    #get the names and teams of players
    i=0
    names = ("\n".join([img['alt'] for img in gdpPlayers.find_all('img', alt=True)]))
    names = names.split('\n')
    for line in names:
        if i%2==0:
            names_table.append(line)
        else:
            teams_table.append(line)
        i=i+1

    #get the links to player stats page
    i=0
    for link in gdpPlayers.find_all('a'):
        #catch link every two link, cause it gets all links twice
        if i%2==0:
            link = link.get('href')
            #change link so it can be user directly
            link = link[8:]
            link = "https://www.plusliga.pl/statsPlayers" + link
            links_table.append(link)
        i=i+1
    
    #getting the positions of players
    for data in gdpPlayers.findAll("div", {"class": "playerposition"}):
        positions_table.append(data.text.strip())
        

    



getPlayers()