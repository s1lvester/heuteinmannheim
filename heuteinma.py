# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import facebook
import websites
import feeds
#import beachstatus
from event import EventVault
import logging
import datetime
import time
import locale

locale.setlocale(locale.LC_TIME, '')  # locale for date, time an the infamous german "Umalaute"

LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'log.log')
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)


class HeuteInMannheim:

    def __init__(self):
        super(HeuteInMannheim, self).__init__()
        self.vault = EventVault()  # Initialize main Storage Object

        # Initialize Scrapers
        self.facebook_scraper = facebook.FacebookScraper(self.vault)
        self.website_scraper = websites.WebsiteScraper(self.vault)
        self.feed_scraper = feeds.FeedScraper(self.vault)

        self.events = self.vault.get_events_for_date(datetime.date.today())
        #self.events = self.vault.get_all_events()  # Only for testing/debugging

#        self.beach_status = beachstatus.BeachStatus()
#        self.beach_status = self.beach_status.get_status()

        self.state_output = self.make_html()
        self.write_html()  # Make initial index.html

        logging.info("Total amount of Events: " + str(len(self.vault.get_all_events())))

        #self.loop()  # Currently not used, since I use Cronjobs

    def loop(self):
        """Function to implement a main-loop.
        Repopulates self.events and regenerates self.state_output if it differs."""
        while True:
            time.sleep(3600)
            logging.info("Getting new Events...")
            self.facebook_scraper.go()
            self.website_scraper.go()
            self.feed_scraper.go()
            self.events = self.vault.get_events_for_date(datetime.date.today())
            newstate_output = self.make_html()
            if self.state_output == newstate_output:
                logging.info("New state! --> new HTML!")
                self.state_output = newstate_output
                self.write_html()

    def make_html(self):
        """Generate HTML output from collected events"""
        output = """<!DOCTYPE html>
        <html>
        <head>
            <title>Heute in Mannheim</title>
            <link href="style.css" media="all" rel="stylesheet" type="text/css">
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <meta name="description" content="Heute in Mannheim ist eine simple Website, die dir Events in Mannheim anzeigt. Unabhängig, werbefrei, unkommerziell, free as in freedom and free as in beer.">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <script type="text/javascript" src="piwik.js"></script>
        </head>
        <body>
        <table>\n"""

        if not self.events:  # Guess we're staying home tonight...
            output += "<tr><td><p><span class=\"title\">Heute keine Events.<br> Guess we're staying home tonight... :-(</span></p></td></tr>\n"
        else:
            eo = 0  # Even/Odd table-rows
            for event in self.events:
                if eo == 0:
                    output += "                             <tr class=\"even\">"
                    eo = 1
                else:
                    output += "                             <tr class=\"odd\">"
                    eo = 0
                # Facebook Icon by http://shimmi1.deviantart.com/ to warn Users from evil Facebook links
                if event.get("event_url").find("facebook") > -1:
                    output_fb = "<img src=\"img/fb_ico.png\" alt=\"Achtung: Facebook Link!\">"
                else:
                    output_fb = ""

                output += """
                             <td><p><span class=\"title\"><a href=\"{}\">{} {}</a></span></p>
                             <span class=\"location\"><a href=\"{}\">{}</a></span><br>
                             <span class=\"adresse\">{} {} | {} {}</span></td>
                             <td><span class=\"zeit\">{}</span><br>
                             </tr>\n""".format(event.get("event_url"),
                                               event.get("title"),
                                               output_fb,
                                               event.get("url"),
                                               event.get("name"),
                                               event.get("strasse"),
                                               event.get("hausnr"),
                                               event.get("plz"),
                                               event.get("ort"),
                                               event.get("uhrzeit"))

#        output += """
#        </table>
#        <hr>
#        <p><b>Status der Mannheimer Strände:</b></p>
#        <table>"""
#        for beach in self.beach_status:
#            hours = ""
#            if beach["status"] == "open":
#                hours = str("<b>" + beach["hours_open"] + " - " + beach["hours_closed"] + "</b><br>")
#            output += """
#            <tr class=\"beach\">
#            <td class=\"{}\">
#                <span class=\"adresse"><a href=\"{}\">{}: {}</a></span><br>
#                {}
#                {} {} | {} {}
#            </td>
#            </tr>""".format(beach["status"],
#                            beach["event_obj"].get("url"),
#                            beach["event_obj"].get("name"),
#                            beach["status"],
#                            hours,
#                            beach["event_obj"].get("strasse"),
#                            beach["event_obj"].get("hausnr"),
#                            beach["event_obj"].get("plz"),
#                            beach["event_obj"].get("ort"))
        output += """
        </table>
        <hr>
        <p><b><a href=\"imprint.html\">Contact, Impressum und Datenschutz</a></b></p>
        <p class=\"footer\">Heute in Mannheim ist eine automatisch generierte Website und wurde nach bestem Wissen und Gewissen erstellt. Die Einträge wurden nicht redaktionell bearbeitet und ich übernehme keinerlei Haftung für die Inhalte hinter den links. Viel Spaß.</p>
        <p class=\"footer\"><a href=\"https://github.com/s1lvester/heuteinmannheim\">Fork me on GitHub</a><br>Danke an die Jungs von <a href=\"http://heuteinstuttgart.de/\">heuteinstuttgart.de</a></p>
        </body>
        </html>"""

        return output

    def write_html(self):
        """Write the index.html file. Requires self.state_output to be set"""
        f = open(os.path.join(os.path.dirname(__file__), "static/index.html"), "w")
        f.write(self.state_output)
        f.close()

# Gooo !!!!11einself
main_obj = HeuteInMannheim()