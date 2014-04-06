# -*- coding: utf-8 -*-

import datetime
from websites import WebsiteScraper
from event import Event
import logging
import traceback
import requests


class BeachStatus:
    """Gather Information from Mannheim's beach-club locations wether they're open or closed"""
    def __init__(self):
        self.beaches = []

    def get_status(self):

        # Neckarstrand Mannheim
        try:
            status_neckarstrand = {}
            soup = WebsiteScraper.make_soup(self=None, url="http://www.neckarstrand-mannheim.de/")
            soup = soup.find("h2", attrs={"align": "right"})
             ###Status is not reliable.
            if soup.text.find("Geöffnet") > -1:  # open
                status_neckarstrand["status"] = "open"
            else:
                status_neckarstrand["status"] = "no_data"
            status_neckarstrand["hours_open"] = "12:00"
            status_neckarstrand["hours_closed"] = "24:00"
            status_neckarstrand["event_obj"] = Event(35, "BeachStatus", datetime.date.today(), "")
            self.beaches.append(status_neckarstrand)
        except:
            logging.error("Error while beachscraping for Neckarstrand: %s" % traceback.format_exc())

        # OEG City-Beach
        # They seem to change status via an image-url in their blog.
        # So I try to check for image IDs
        try:
            status_oeg = {}
            r = requests.get("http://oeg-citybeach.de/open/")
            if r.text.find("xmp.did:12D3ABFA7F4111E2A395BC8F330BA798") > -1:  # open
                status_oeg["status"] = "open"
            elif r.text.find("xmp.did:0880117407206811822ACEA8F488BC6D") > -1:  # closed
                status_oeg["status"] = "closed"
            else:  # No info...
                status_oeg["status"] = "no_data"
            status_oeg["event_obj"] = Event(13, "BeachStatus", datetime.date.today(), "")  # Create an event to gather Info from DB
            # Hours:
            #    Mo - Fr: 16.00 - 01.00 Uhr
            #    Sa + So: 12.00 - 01.00 Uhr
            if datetime.date.weekday(datetime.date.today()) < 5:  # Buisenenss Day :-(
                status_oeg["hours_open"] = "16:00"
            else:  # Weekend! :-)
                status_oeg["hours_open"] = "12:00"
            status_oeg["hours_closed"] = "01:00"
            self.beaches.append(status_oeg)
        except:
            logging.error("Error while beachscraping for OEG City Beach: %s" % traceback.format_exc())

        # Playa del Ma
        try:
            status_playadelma = {}
            r = requests.get("http://www.playadelma.de/rss.php")
            if r.text.find("OPEN") > -1:
                status_playadelma["status"] = "open"
            elif r.text.find("CLOSED") > -1:
                status_playadelma["status"] = "closed"
            else:
                status_playadelma["status"] = "no_data"
            # Hours:
            #    Mon - Thu: 15:00 - 01:00
            #    Fri - Sat: 15:00 - 03:00
            #    Sun: 15:00 - 00:00
            status_playadelma["hours_open"] = "15:00"
            if datetime.date.weekday(datetime.date.today()) == 4 or datetime.date.weekday(datetime.date.today()) == 5:
                status_playadelma["hours_closed"] = "03:00"
            elif datetime.date.weekday(datetime.date.today()) == 6:
                status_playadelma["hours_closed"] = "00:00"
            else:
                status_playadelma["hours_closed"] = "01:00"
            status_playadelma["event_obj"] = Event(14, "BeachStatus", datetime.date.today(), "")
            self.beaches.append(status_playadelma)
        except:
            logging.error("Error while beachscraping for Playa del Ma: %s" % traceback.format_exc())

        return self.beaches