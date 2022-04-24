# importing the libraries
from glob import glob
from numpy import zeros
from bs4 import BeautifulSoup
import requests
import win32com.client as win32
import os
import shutil
import xlwings as xw
from datetime import date

zawodnicy = 2
srodkowi = 2
atakujacy = 2
libero = 2
przyjmujacy = 2
rozgrywajacy = 2
    

def getData(name, team, url, position):
    global zawodnicy
    global srodkowi
    global atakujacy
    global libero
    global przyjmujacy
    global rozgrywajacy

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
    if a[0] > 20:
             
        

        data = ','.join(str(e) for e in a)
        data = name + ',' + team + ',' + position + ',' + data
        data = data.split(',')

        if float(data[14]) != 0:
            skut = ((float(data[17])-float(data[16])-float(data[15]))*100)/float(data[14])
        else:
            skut = 0

        data.insert(19, str('%.2f'%skut))
        pos = 'A' + str(zawodnicy)
        sheet1.range(pos).value = data
        zawodnicy = zawodnicy + 1


        if position == "atakujący":
            pos = 'A' + str(atakujacy)
            sheet2.range(pos).value = data
            atakujacy = atakujacy + 1
                    
        if position == "rozgrywający":
            pos = 'A' + str(rozgrywajacy)
            sheet3.range(pos).value = data
            rozgrywajacy = rozgrywajacy + 1
                    
        if position == "przyjmujący":
            pos = 'A' + str(przyjmujacy)
            sheet4.range(pos).value = data
            przyjmujacy = przyjmujacy + 1
                    
        if position == "środkowy":
            pos = 'A' + str(srodkowi)
            sheet5.range(pos).value = data
            srodkowi = srodkowi + 1
                    
        if position == "libero":
            pos = 'A' + str(libero)
            sheet6.range(pos).value = data
            libero = libero + 1


def getPlayers():
    #Make a GET request to fetch the raw HTML content
    htmlPlayers = requests.get("https://www.plusliga.pl/players.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D").text

    #Parse the html content
    soupPlayers = BeautifulSoup(htmlPlayers, "html.parser")

    #Get the table having the div 
    gdpPlayers = soupPlayers.find("div", id="hiddenPlayersListAllBuffer")

    #for players data
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
        
    #get the stats of every player
    for i in range(len(names_table)):
        getData(names_table[i], teams_table[i], links_table[i], positions_table[i])      



# Open existing Workbooks
wb = xw.Book('zawodnicy.xlsx')  
sheet1 = wb.sheets['zawodnicy']
sheet2 = wb.sheets['atakujacy']
sheet3 = wb.sheets['rozgrywajacy']
sheet4 = wb.sheets['przyjmujacy']
sheet5 = wb.sheets['srodkowi']
sheet6 = wb.sheets['libero']

#adding headers
sheet1.range('A1').value = ['Nazwisko', 'Klub', 'Pozycja', 'Liczba setów', 'Punkty', 'Suma zagrywek', 'Asy serwisowe', 'Błędy na zagrywce', 'Asy na set', 'Suma przyjęć', 'Błędy w przyjęciu', 'Negatywne przyjęcia', 'Przyjęcia', '% przyjęcia', 'Suma ataków', 'Błędy w ataku', 'Zablokowane ataki', 'Skończone ataki', '% Skuteczności ataku', '% efektywności ataku', 'Bloki', 'Bloki na set']
sheet2.range('A1').value = ['Nazwisko', 'Klub', 'Pozycja', 'Liczba setów', 'Punkty', 'Suma zagrywek', 'Asy serwisowe', 'Błędy na zagrywce', 'Asy na set', 'Suma przyjęć', 'Błędy w przyjęciu', 'Negatywne przyjęcia', 'Przyjęcia', '% przyjęcia', 'Suma ataków', 'Błędy w ataku', 'Zablokowane ataki', 'Skończone ataki', '% Skuteczności ataku', '% efektywności ataku', 'Bloki', 'Bloki na set']
sheet3.range('A1').value = ['Nazwisko', 'Klub', 'Pozycja', 'Liczba setów', 'Punkty', 'Suma zagrywek', 'Asy serwisowe', 'Błędy na zagrywce', 'Asy na set', 'Suma przyjęć', 'Błędy w przyjęciu', 'Negatywne przyjęcia', 'Przyjęcia', '% przyjęcia', 'Suma ataków', 'Błędy w ataku', 'Zablokowane ataki', 'Skończone ataki', '% Skuteczności ataku', '% efektywności ataku', 'Bloki', 'Bloki na set']
sheet4.range('A1').value = ['Nazwisko', 'Klub', 'Pozycja', 'Liczba setów', 'Punkty', 'Suma zagrywek', 'Asy serwisowe', 'Błędy na zagrywce', 'Asy na set', 'Suma przyjęć', 'Błędy w przyjęciu', 'Negatywne przyjęcia', 'Przyjęcia', '% przyjęcia', 'Suma ataków', 'Błędy w ataku', 'Zablokowane ataki', 'Skończone ataki', '% Skuteczności ataku', '% efektywności ataku', 'Bloki', 'Bloki na set']
sheet5.range('A1').value = ['Nazwisko', 'Klub', 'Pozycja', 'Liczba setów', 'Punkty', 'Suma zagrywek', 'Asy serwisowe', 'Błędy na zagrywce', 'Asy na set', 'Suma przyjęć', 'Błędy w przyjęciu', 'Negatywne przyjęcia', 'Przyjęcia', '% przyjęcia', 'Suma ataków', 'Błędy w ataku', 'Zablokowane ataki', 'Skończone ataki', '% Skuteczności ataku', '% efektywności ataku', 'Bloki', 'Bloki na set']
sheet6.range('A1').value = ['Nazwisko', 'Klub', 'Pozycja', 'Liczba setów', 'Punkty', 'Suma zagrywek', 'Asy serwisowe', 'Błędy na zagrywce', 'Asy na set', 'Suma przyjęć', 'Błędy w przyjęciu', 'Negatywne przyjęcia', 'Przyjęcia', '% przyjęcia', 'Suma ataków', 'Błędy w ataku', 'Zablokowane ataki', 'Skończone ataki', '% Skuteczności ataku', '% efektywności ataku', 'Bloki', 'Bloki na set']

getPlayers()

src = 'zawodnicy.xlsx'
dst = str(date.today())+'.xlsx'
shutil.copyfile(src, dst)