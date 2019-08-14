import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from collections import defaultdict,namedtuple


#Return the     
def getLinesOfToplist(InputSoup) -> list:
    soup = InputSoup
    N = namedtuple("N", "number, artist, title, position")
    Lines = []
    ulsoup = soup.find("ul").find_all("li")
    for line in soup.find("ul").find_all("li"):
        _number = line.find("div", class_="number").get_text()
        _artist = line.find("div", class_="artist").get_text()
        _title = line.find("div", class_="title-track").get_text()
        _position = line.find("div", class_="position").get_text()
        Lines.append(N(number=_number,artist=_artist,title=_title,position=_position))
    return Lines
    


#Returns structure of the website parsed by Beautiful soup
def getSoupFormatOfSite(URL: str): 
    response = requests.get(URL)
    return BeautifulSoup(response.content, "html.parser")

#Returns link to the most recent Toplist
def getTheMostRecentToplistLink(soup) -> str: 
    Target = soup.find("a", id=re.compile("LinkArea:Vote\d*"))
    return "https://www.antyradio.pl" + Target["href"]

#Main Function
def main():
    MainURL = "https://www.antyradio.pl/Radio/Turbo-Top" #Main URL to get the latest Toplist
    MainSoup = getSoupFormatOfSite(MainURL)
    WantedURL = getTheMostRecentToplistLink(MainSoup)
    TargetSoup = getSoupFormatOfSite(WantedURL)
    for line in getLinesOfToplist(TargetSoup):
        print(f"{line.number}. {line.artist}\"{line.title[1:]}\"\t{line.position}")

#Run main function
if __name__ == "__main__":
    main()