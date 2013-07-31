# -*- coding: utf-8 -*-
import requests
import dateutil.parser as dparser
import logging
from event import Event


class FacebookGraph:
    """Connects to the facebook graph API and builds Requests.
    Relies on an access token which is created via an facebook app.
    see: https://developers.facebook.com/docs/facebook-login/access-tokens/#generating
    also you'll need a facebook developer account to crate an app whicht you'll need
    to get the client_credientials"""
    def __init__(self):
        super(FacebookGraph, self).__init__()
        # Get Access Token
        r = requests.get('https://graph.facebook.com/oauth/access_token',
                         params={"client_id": "",
                                 "client_secret": "",
                                 "grant_type": "client_credentials"})
        self.access_token = r.text.split('=')[1]

    def get(self, fb_url):
        url = "https://graph.facebook.com/" + fb_url
        r = requests.get(url, params={"access_token": self.access_token})
        logging.debug("Facebook-URL:" + r.url)
        return r.json()


class FacebookScraper:
    """Scraper for Facebook events using the graph API"""
    graph = str()
    # List of Facebook sites with their ID in the sqlite-DB (in Mannheim)
    fb_sites = [[4, "loftclubludwigshafen", "Loft Club"],  # Some Sites need Specific Locations
                [5, "hafen49", "Hafen 49"],
                [6, "dieKuecheMannheim"],
                [7, "discozwei"],
                [8, "hagestolzbar"],
                [9, "nelsonjungbuschbar"],
                [10, "peer23"],
                [11, "sohomannheim"],
                [12, "oegcitybeach", "OEG CITYBEACH"],
                [14, "playadelma"],
                [15, "BlauJungbusch"],
                [16, "daszimmer"],
                [17, "genesismannheim"],
                [18, "koiclubmannheim"],
                [19, "MSConnexion"],
                [20, "cluboc"],
                [21, "clubritzz"],
                [22, "batonrouge.mannheim"],
                [23, "The-Suite"],
                [26, "ZumTeufel"],
                [27, "Filmriss.bar"],
                [30, "zapatto.mannheim"],
                [31, "AlteSeilerei"],
                [32, "Bootshaus"],
                [33, "bockmannheim"],
                # The following are "old" Facebook pages which only provide an ID
                [24, "114510748568298"],  # JUZ Mannheim
                [28, "167521296599554"],  # O-Ton
                [29, "108785689188333"],  # Contra-N
                [34, "158338344184558"],  # Cafe Vienna
                [35, "149332661794551"],  # Neckarstrand-Mannheim
                [36, "152321714945335"],  # Quartiermanagement Neckarstadt-West
                [37, "NORD.Coffee.Wine.Bar"],
                [38, "zwischenraumma"],
                [39, "Fitzgeralds.Irish.Pub"]
                ]

    def __init__(self, vault):
        self.vault = vault
        self.graph = FacebookGraph()
        self.go()

    def go(self):
        for site in self.fb_sites:
            if len(site) == 3:  # If Location is set
                self.scrape(db_id=site[0], fb_site=site[1], location=site[2])
            else:
                self.scrape(db_id=site[0], fb_site=site[1])

    def scrape(self, db_id, fb_site, location=False):

        res_data = self.graph.get(fb_site + "/events?limit=5000")

        for fb_event in res_data["data"]:  # Print the res_data to see why...
            # Some pages require a specific location because they publish events for several
            # "affilliated" locations for which the adress data in the sqlite db doesn't match
            if not location or (location and fb_event["location"] == location):
                datum = dparser.parse(fb_event["start_time"], fuzzy=True)  # dparser: so simple...
                e = Event(db_id,
                          fb_event["name"],
                          datum,
                          "https://www.facebook.com/events/" + fb_event["id"])
                self.vault.add(e)
