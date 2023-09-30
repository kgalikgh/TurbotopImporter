import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from collections import defaultdict,namedtuple
   
def getLinesOfToplist(InputSoup) -> list:
    soup = InputSoup
    Lines = []
    ulsoup = soup.find("ul").find_all("li")
    for line in soup.find("ul").find_all("li"):
        _number = line.find("div", class_="number").get_text()
        _artist = line.find("div", class_="artist").get_text()
        _title = line.find("div", class_="title-track").get_text()[1:]
        _position = line.find("div", class_="position").get_text()
        Lines.append([_number,_artist,_title,_position])
    return Lines
    
#Returns structure of the website parsed by Beautiful soup
def getSoupFormatOfSite(URL: str): 
    response = requests.get(URL)
    return BeautifulSoup(response.content, "html.parser")

#Returns link to the most recent Toplist
def getTheMostRecentToplistLink(soup) -> str: 
    Target = soup.find("a", id=re.compile("LinkArea:Vote\d*"))
    return "https://www.antyradio.pl" + Target["href"]

def printTable(targetSoup):
    size = max(map(lambda x: sum(map(lambda y: len(y), x)),targetSoup))
    print(str.center("TURBO TOP LIST",size,"="))
    for line in targetSoup:
        print(str.center("{}. {} - {} {}\n".format(*line),size))
        print(size*'=')
       
#Main Function
def main():
    MainURL = "https://www.antyradio.pl/Radio/Turbo-Top" #Main URL to get the latest Toplist
    MainSoup = getSoupFormatOfSite(MainURL)
    WantedURL = getTheMostRecentToplistLink(MainSoup)
    TargetSoup = getSoupFormatOfSite(WantedURL)
    Lines = getLinesOfToplist(TargetSoup)
    printTable(Lines)

#Run main function
if __name__ == "__main__":
    main()
