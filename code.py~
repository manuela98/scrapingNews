import requests
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime



def findHour(article):
    """Find the hour in an article."""
    find = article.findAll("div", {"class": "categoria-noticia"})
    hour = ''
    date = ''
    if len(find[0].text.split('|')[-1].split())==2:
        hour = find[0].text.split('|')[-1]
    else: 
        date = find[0].text.split('|')[-1]
    if date=='':
       date= datetime.today()
       date = date.strftime("%d/%m/%Y")
    return hour,date


def getInformation(page):
    """Get the titles of a page in a file and hours"""
    data = []
    soup = BeautifulSoup(page.text, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        try:
            if  article.findAll("div", {"class": "categoria-noticia"}):
                title = article.findAll("span", {"class": "priority-content"})[0].text
                title = title.encode('latin1').decode('utf-8')
                hour,date = findHour(article)
                data+=[[str(title),'Colombiano',date,hour]]
        except: 
            pass
    
    return data


def writeCsv(page):
    """Write a csv with: titular, medio, fecha, hora"""
    date= datetime.today()
    date = date.strftime("%d-%m-%Y")
    title = str(date)
    data = getInformation(page)
    df = pd.DataFrame(data, columns = ['titular','medio', 'fecha','hora']) 
    df.to_csv(title+'_Colombiano.csv',index=False)
    return None 


def pageRequests():
    """Request the menu page and get the titles."""
    print('https://www.elcolombiano.com/')
    page = requests.get('https://www.elcolombiano.com/')    
    writeCsv(page)
    return None

    

   

pageRequests()

