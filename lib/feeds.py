# -*- coding: utf-8 -*-

import feedparser
import dateutil.parser as dparser
from event import Event


class FeedScraper:
    """Simple Scraper for RSS/Atom feeds using the feedparser lib
    at http://code.google.com/p/feedparser"""
    def __init__(self, vault):
        self.vault = vault
        self.go()

    def go(self):
        # Alte Feuerwache Mannheim: altefeuerwache.com
        f = feedparser.parse("http://www.altefeuerwache.com/programm/monatsprogramm/atom.xml")
        for i in range(len(f["entries"])):
            datum = f.entries[i]["title"].split("|")
            datum = dparser.parse(datum[1], dayfirst=True, fuzzy=True)
            title = f.entries[i]["title"].split("|")
            title = str(title[0].strip())
            e = Event(1,
                      title,
                      datum,
                      f.entries[i]["link"].strip())
            self.vault.add(e)