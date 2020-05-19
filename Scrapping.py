import requests
from bs4 import BeautifulSoup
import time
"""
links = []

for i in range(26):
    url = 'http://example.webscrapping.com/places/default/index' + str(i)
    response = requests.get(url)
    print(response)
    if response.ok:
        print('Page: ' + str(i))
        soup = BeautifulSoup(response.text, 'lxml')
        tds = soup.findAll('td')
        for td in tds:
            a = td.find('a')
            link = a['href']
            links.append('http://example.webscrapping.com' + link)
        time.sleep(3)

print(len(links))
   
with open('urls.txt', 'w') as file:
    for link in links:
        file.write(link + '\n')

"""
with open('urls.txt', 'r') as inf:
    with open('pays.csv', 'w') as outf:
        outf.write('pays, population\n')
    for row in inf:
        url = row.strip()
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            country = soup.find('tr', {'id' : 'places_country__row'}).find('td', {'class': 'w2p_fw'})
            pop = soup.find('tr', {'id' : 'places_population__row'}).find('td', {'class': 'w2p_fw'})
            print('Pays: ' + country.text + ', Pop: ' + pop.text)
            outf.write(country.text + ',' + pop.text.replace(',', '') + '\n')
        time.sleep(3)