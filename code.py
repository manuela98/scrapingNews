import requests
from bs4 import BeautifulSoup


categories = ['antioquia','colombia','internacional','negocios','deportes','opinion']



def getTitles(page,fileTitles):
    
    '''Get the titles of a page in a file'''
    
    soup = BeautifulSoup(page.text, 'html.parser')
    articulos = soup.find_all('article')
    for articulo in articulos:
        try:
            titulo = articulo.span.text.encode('latin-1','ignore')
            fileTitles.write(titulo)
            fileTitles.write('\n')
        except: 
            pass
    
    return fileTitles


def MenuSelection(categories):

    '''Request the menu page and get the titles'''

    file = open('titles.txt','w+')
    for i in categories:
        print('https://www.elcolombiano.com/'+i)
        page = requests.get('https://www.elcolombiano.com/'+i)
        getTitles(page,file)
    file.close()
    return 0

def FileProcessing(fileName):
    
    '''remove the duplications and order the news'''
   
    data=file(fileName).readlines()
    data = set(data)
    data = sorted(data)
    fileFiltered = open('filteredTitles.txt','w+')
    for i in range(4,len(data)):
         fileFiltered.write(data[i])
         fileFiltered.write('\n')
   

MenuSelection(categories)
FileProcessing('titles.txt')
