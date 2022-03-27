# importing the libraries
from numpy import zeros
from bs4 import BeautifulSoup
import requests
import csv  
import numpy
import pandas as pd
import re

url="https://www.plusliga.pl/statsPlayers/id/304.html"

#Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

#Parse the html content
soup = BeautifulSoup(html_content, "lxml")



#Get the table having the class wikitable
gdp_table = soup.find("table", attrs={"class": "rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive"})
gdp_table_data = gdp_table.tbody.find_all("tr")  # table
#print(gdp_table_data)

column_names = ["mecz", "sety", "suma zagrywek", "asy", "błędy zagrywki", "asy na set", "suma przyjęć", "błędy przyjęć", "przyjęcia negatywne", "suma ataków", "błędy ataków", "zablokowane ataki", "skończone ataki", "%skuteczności", "bloki", "bloki na set"]

i=0
a = zeros(18, float)
list = []
for td in gdp_table.find_all("tr"):
    #print(td.text)
    tekst = td.text
    tekst=tekst.split()
    if "Łącznie" in tekst:
        for xd in tekst:
            try:
                xd = xd.replace(',','.')
                list.append(xd)
                a[i]=float(xd)
                i=i+1
            except ValueError:
                pass    
print(a)
print(list)

a = pd.DataFrame(a)
a.to_csv('staty.csv', float_format='%.3f', index=False)
