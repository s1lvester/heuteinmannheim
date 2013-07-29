# -*- coding: utf-8 -*-

import os
import logging
import sqlite3


class Event:
    """Class representing a single Event."""
    def __init__(self, db_id, title, datum, url):
        self.data = dict()

        # Get Information for this event from the sqlite DB
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "../locations.sqlite"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('select * from locations where id=?', [db_id])
        r = c.fetchone()

        for key in list(r.keys()):  # Populate list with data from database
            self.data[key] = r[key]

        # Populate list with data from web
        self.data["title"] = title
        self.data["datetime"] = datum
        self.data["datum"] = datum.strftime("%a, %d. %b")
        uhrzeit = datum.strftime("%H:%M")
        if uhrzeit == "00:00":  # "probably" no specific time set for this event...'
            uhrzeit = ""
        self.data["uhrzeit"] = uhrzeit  # uhrzeit = german time
        self.data["event_url"] = url

        logging.info(" Found Event: " + str(self.data["title"]) + " at " + str(self.data["name"]))

    def get(self, param):
        return self.data[param]

    def getall(self):
        return self.data


class EventVault:
    """Central Storage for events"""
    def __init__(self):
        self.events = []

    def add(self, e):
        self.events.append(e)

    def get_events_for_date(self, date):
        e_subset = []
        for e in self.events:
            if e.get("datetime").date() == date:
                e_subset.append(e)

        if len(e_subset) > 0:
            e_subset = sorted(e_subset, key=lambda e: e.data["uhrzeit"])  # Sort by uhrzeit
            return e_subset
        else:
            return False

    def get_all_events(self):
        if len(self.events) > 0:
            return self.events
        else:
            return False