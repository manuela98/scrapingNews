import requests
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime,timedelta

def writeCsv(page,medium,getInformation):
    """Write a csv with: titular, medio, fecha, hora."""
    date= datetime.today()
    date = date.strftime("%d-%m-%Y")
    title = str(date)
    data = getInformation(page)
    df = pd.DataFrame(data, columns = ['Titular','Medio', 'Fecha','Hora']) 
    df.to_csv(title+'_'+medium+'.csv',index=False)
    return None 


def pageRequests(page,medium,getInformation):
    """Request the menu page and get the titles."""
    print(page)
    page = requests.get(page)    
    writeCsv(page,medium,getInformation)
    return None

    


def findHourColombiano(article):
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


def getInformationColombiano(page):
    """Get the titles of a page in a file and hours."""
    data = []
    soup = BeautifulSoup(page.text, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        try:
            if  article.findAll("div", {"class": "categoria-noticia"}):
                title = article.findAll("span", {"class": "priority-content"})[0].text
                title = title.encode('latin1').decode('utf-8')
                hour,date = findHourColombiano(article)
                data+=[[str(title),'Colombiano',date,hour]]
        except: 
            pass
    
    return data

def getHourDateEspectador(text):
    """Get hour and date from Espectador."""
    hour = ''
    date = ''
    try: 
        if isinstance(int(text[0]), int):
            date = datetime.today()-timedelta(days=1)
            date = date.strftime("%d/%m/%Y")
    except:
        hour = text.split(' ')
        if hour[2]=='horas' or hour[2]=='hora':
           dateTitle= datetime.today()- timedelta(hours=int(hour[1]))
           hour = dateTitle.strftime("%I:%M %p")
           date =  dateTitle.strftime("%d/%m/%Y")
        if hour[2]=='mins':
           dateTitle= datetime.today()- timedelta(minutes=int(hour[1]))
           hour = dateTitle.strftime("%I:%M %p")
           date =  dateTitle.strftime("%d/%m/%Y")

    return hour,date

def getInformationEspectador(page):
    """Get information page Espectador titulo,medio,fecha,hora."""
    data = []
    soup = BeautifulSoup(page.text, 'html.parser')
    articles = soup.findAll("div", \
    {"class":"required-fields group-text-content field-group-html-element"})
    for article in articles:
        title =  article.findAll("div", \
        {"class":"node-title field field--name-title field--type-ds field--label-hidden"})
        hour =  article.findAll("div", \
        {"class":"node-post-date field field--name-post-date field--type-ds field--label-hidden"})
        try:
            title = title[0].text[:-32]
            hour,date =  getHourDateEspectador(hour[0].text)
            data+=[[str(title),'Espectador',date,hour]]
        except:
            pass
    return data

def getInformationTiempo(page):
    """Get information page Tiempo titulo,medio,fecha,hora."""
    data = []
    soup = BeautifulSoup(page.text, 'html.parser')
    articles = soup.findAll("div", \
    {"class":"article-details"})
    for article in articles:
        
        try:
           title = article.findAll("h3",{"class":"title-container"})[0].text
           hour = article.findAll("div",{"class":"category-published"})[0].span.text
           date =  datetime.today()
           date =  date.strftime("%d/%m/%Y")
           data+=[[str(title),'Tiempo',date,hour]]
        except:
           pass 
    return data

def getInformationXataka(page):
    """Get information page Xataka titulo,medio,fecha,hora."""
    soup = BeautifulSoup(page.text, 'html.parser')
    articles =  soup.findAll("div",{"class":"abstract-content"})
    data = []
    for article in articles:
        title = article.findAll("h2",{"class":"abstract-title"})[0].text
        hourDate = article.findAll("time",{"class":"abstract-date"})[0]
        date = hourDate['datetime'].split('T')[0]
        date = date.split('-')
        date = datetime(int(date[0]),int(date[1]),int(date[2]))
        date =  date.strftime("%d/%m/%Y")
        hour = hourDate['datetime'].split('T')[1][:-6]
        hour = hour.split(':')
        today = datetime.today().replace(hour=int(hour[0]), minute=int(hour[1]))
        hour = today.strftime("%I:%M %p")
        data+=[[str(title),'Xataka',date,hour]]
    return data


pageRequests('https://www.elcolombiano.com/','Colombiano',getInformationColombiano)
pageRequests('https://www.elespectador.com/noticias','Espectador',getInformationEspectador)
pageRequests('https://www.eltiempo.com/','Tiempo',getInformationTiempo)
pageRequests('https://www.xataka.com/','Xataka',getInformationXataka)
