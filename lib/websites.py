# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import dateutil.parser as dparser
import datetime
import logging
from event import Event


class WebsiteScraper:
    """Simple Website Scraping using the BeautifulSoup lib (Version 4) + requests"""
    def __init__(self, vault):
        self.vault = vault
        self.go()

    def make_soup(self, url):
        """Request an URL and generate an bs4 Object from the result"""
        r = requests.get(url)
        if r.ok:  # True when 200 OK
            return(BeautifulSoup(r.text))
        else:
            logging.error("URL-Error: " + url)
            return False

    def go(self):

        # Capitol-Mannheim.de
        soup = self.make_soup("http://www.capitol-mannheim.de/spielplan")
        if soup:
            terminfeld = soup.find_all("div", attrs={"class": "views-field views-field-field-kategorie"})
            for i in range(len(terminfeld)):
                datum = dparser.parse(terminfeld[i].find("span")["content"], fuzzy=True)
                contentfeld = soup.find_all("div", attrs={"class": "views-field views-field-field-claim"})
                e = Event(2,
                          contentfeld[i].find("a").text,
                          datum,
                          contentfeld[i].find("a")["href"])
                self.vault.add(e)

        # SAParena.de
        soup = self.make_soup("http://saparena.de/events/")
        if soup:
            content_blocks = soup.find_all("div", attrs={"class": "post-content"})
            if len(content_blocks) < 1:
                logging.error("Cannot Scrape SAParena.de")
            for content_block in content_blocks:
                termin_block = content_block.find("time", attrs={"class": "post-date"})
                datum = dparser.parse(termin_block["datetime"], fuzzy=True)
                e = Event(25,
                          content_block.find("span", attrs={"itemprop": "name"}).text,
                          datum,
                          str("http://saparena.de" + content_block.find("a", attrs={"itemprop": "url"})["href"]))
                self.vault.add(e)

        ## ZeitraumExit.de
        #soup = self.make_soup("http://www.zeitraumexit.de/programm/uebersicht")
        #if soup:  # URL ist 200 OK
            #rows = soup.find_all("tr")
            #if len(rows) < 1:
                #logging.error("Cannot scrape zeitraumexit.de")
            #for row in rows:
                #datum = row.find('td', attrs={'class': 'date'}).text + " " + row.find('td', attrs={'class': 'time'}).text
                #datum = dparser.parse(datum, dayfirst=True, fuzzy=True)
                #link = row.find('td', attrs={'class': 'title'}).find('a', href=True)
                #e = Event(3,
                          #row.find('td', attrs={'class': 'title'}).a.contents[0],
                          #datum,
                          #"http://www.zeitraumexit.de" + link["href"])
                #self.vault.add(e)
