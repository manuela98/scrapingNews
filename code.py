import requests
from bs4 import BeautifulSoup
import codecs

categories = ['antioquia','colombia','internacional','negocios','deportes','opinion']



def getTitles(page,f):
    
    '''Get the titles of a page in a file'''

  
    soup = BeautifulSoup(page.text, 'html.parser')
    articulos = soup.find_all('article')
    for articulo in articulos:
        try:
            titulo = articulo.span.text
            f.write(titulo.encode('latin1').decode('utf-8'))
            f.write('\n')
        except: 
            pass
    
    return 0


def MenuSelection(categories):

    """Request the menu page and get the titles"""
    f = open('titles.txt','w+')
    for i in categories:
        print('https://www.elcolombiano.com/'+i)
        page = requests.get('https://www.elcolombiano.com/'+i)
        getTitles(page,f)
    f.close()
    return 0

def FileProcessing(fileName):
    
    """Remove the duplications and order the news"""
    file = open(fileName)
    data=file.readlines()
    data = set(data)
    data = sorted(data)
    fileFiltered = open('filteredTitles.txt','w+')
    for i in range(4,len(data)):
         fileFiltered.write(data[i])
         fileFiltered.write('\n')
   

MenuSelection(categories)
FileProcessing('titles.txt')
