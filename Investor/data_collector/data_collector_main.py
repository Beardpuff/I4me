# \todo(vrubies) Make script/class that load data from a website and
# saves info to the data folder.

from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
import os
import numpy as np


class WebsiteDataCollector():

    def __init__(self,
                 name,
                 website,
                 initial_address):

        self.name = name
        self.website = website
        self.initial_address = initial_address
        self.initial_has_info = None
        self.parse_links_rules = None
        self.parse_text_rules = None

        # Params used during crawl.
        self.current_website = None
        self.current_has_info = None
        self.current_depth = None

    def check_ready(self):
        assert self.initial_has_info is not None
        assert self.parse_links_rules is not None
        assert self.parse_text_rules is not None

    def crawl(self,
              depth=1,
              verbose=False):
        os.makedirs("./articles", exist_ok=True)
        # Crawler function.
        self.crawl_list = [(address, self.initial_has_info, 0)
                           for address in self.initial_address]
        current_depth = 0

        # Breath first (search) of websites.
        parse_time = 0.0
        parsed_articles = 0
        while len(self.crawl_list) > 0:

            (current_website, current_has_info,
                current_depth) = self.crawl_list.pop(0)

            if verbose and (parsed_articles > 0):
                nlist_e = len(self.crawl_list)
                avg_time = parse_time/parsed_articles
                total_time = nlist_e * avg_time
                print('\rETA={:f} s. Current size of crawl_list = {:d}. Avg_time = {:f}.'.format(
                      total_time, nlist_e, avg_time), end=" ")

            start_time = time.time()
            data = requests.get(current_website).text
            soup = BeautifulSoup(data, 'html.parser')

            if current_has_info:
                # If website has information to be parsed extract data.
                try:
                    info_dict = self.extract_text(soup)
                    if len(info_dict["tickers"]) > 0:
                        info_dict["website"] = current_website
                        file_name = "-".join(info_dict["author_name"])
                        file_name = "_".join(file_name.split()) + "_" + info_dict["date"]
                        # with open("./articles/"+file_name+".json", "w") as outfile:
                        #     json.dump(info_dict, outfile)
                    parsed_articles += 1
                    elapsed_time = (time.time() - start_time)
                    parse_time += elapsed_time
                except:
                    pass
            if current_depth < depth:
                # If crawl_depth is less that max_depth, append new websites.
                try:
                    self.crawl_list += self.extract_links(soup, current_depth)
                except:
                    pass

    def extract_text(self):
        # Parses text from a website.
        raise NotImplementedError

    def extract_links(self):
        # Parses links from a website.
        raise NotImplementedError
