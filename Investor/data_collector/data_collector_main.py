# \todo(vrubies) Make script/class that load data from a website and
# saves info to the data folder.

from bs4 import BeautifulSoup
import requests


class WebsiteDataCollector():

    def __init__(self,
                 name,
                 website,
                 initial_address):

        self.name = name
        self.website = website
        self.crawl_list = [initial_address]
        self.initial_has_info = None
        self.parse_links_rules = None
        self.parse_text_rules = None

        # Params used during crawl.
        self.current_website = None
        self.current_has_info = None
        self.current_depth = None

    def check_ready():
        assert self.initial_has_info is not None
        assert self.parse_links_rules is not None
        assert self.parse_text_rules is not

    def crawl(self,
              depth=0,
              verbose=False):
        # Crawler function.
        self.crawl_list = [(self.initial_address, self.initial_has_info, 0)]

        # Breath first (search) of websites.
        while len(self.crawl_list) > 0:
            if verbose:
                print('\nCurrent size of crawl_list = {:d}'.format(
                      len(self.crawl_list)))
            (current_website, current_has_info,
                current_depth) = self.crawl_list.pop(0)

            data = requests.get(self.initial_address).text
            soup = BeautifulSoup(data, 'html.parser')

            if current_has_info:
                # If website has information to be parsed extract data.
                self.extract_text(soup)
            if current_depth < depth:
                # If crawl_depth is less that max_depth, append new websites.
                self.crawl_list += self.extract_links(soup, current_depth)

    def extract_text(self):
        # Parses text from a website.
        raise NotImplementedError

    def extract_links(self):
        # Parses links from a website.
        raise NotImplementedError
