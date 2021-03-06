# \todo(vrubies) Make script/class that load data from a website and
# saves info to the data folder.

from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
import os
import numpy as np
from collections import OrderedDict
import multiprocessing
from multiprocessing import Pool


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

        self.num_cpus = multiprocessing.cpu_count()

    def check_ready(self):
        assert self.initial_has_info is not None
        assert self.parse_links_rules is not None
        assert self.parse_text_rules is not None

    def crawl(self,
              depth=1,
              verbose=False):
        self.depth = depth
        self.article_root_dir = "./" + self.name + "_articles"
        os.makedirs(self.article_root_dir, exist_ok=True)
        # Crawler function.
        self.crawl_list = [(address, self.initial_has_info, 0)
                           for address in self.initial_address]
        current_depth = 0
        # Breath first (search) of websites.
        parse_time = 0.0
        parse_passes = 0
        while len(self.crawl_list) > 0:
            start_time = time.time()
            nlist_e = len(self.crawl_list)

            args_input = []
            for ii in range(min(self.num_cpus,nlist_e)):
                args_input.append(self.crawl_list.pop(0))
                parse_passes += 1             
            with Pool(len(args_input)) as pool:
                extracted = pool.starmap(self.extract_fcn, args_input)
                for ee in extracted:
                    self.crawl_list += ee

            # Here ends the new stuff.
            # (self.current_website, current_has_info,
            #     current_depth) = self.crawl_list.pop(0)

            # data = requests.get(self.current_website).text
            # soup = BeautifulSoup(data, 'html.parser')

            # if current_has_info:
            #     # If website has information to be parsed extract data.
            #     # try:
            #     info_dict, ignore = self.extract_text(soup)
            #     if not ignore:
            #         info_dict["website"] = self.current_website
            #         self.store_info(info_dict)
            #     # except AssertionError:
            #     #     print("Error!")

            # if current_depth < depth:
            #     # If crawl_depth is less that max_depth, append new websites.
            #     try:
            #         self.crawl_list += self.extract_links(soup, current_depth)
            #     except:
            #         pass

            # Time stats.
            nlist_e = len(self.crawl_list)
            # parse_passes += 1
            elapsed_time = (time.time() - start_time)
            parse_time += elapsed_time
            avg_time = parse_time / parse_passes
            total_time = nlist_e * avg_time
            if verbose:
                print('\rETA={:f} s. Current size of crawl_list = {:d}. Avg_time = {:f}.'.format(
                      total_time, nlist_e, avg_time), end=" ")

    def extract_fcn(self, current_website, current_has_info, current_depth):
        self.current_website = current_website
        data = requests.get(current_website).text
        soup = BeautifulSoup(data, 'html.parser')

        # print("Part I - {:d}".format(os.getpid()), " and ", current_has_info)
        if current_has_info:
            # If website has information to be parsed extract data.
            # try:
            # print("Part II - {:d}".format(os.getpid()))
            info_dict, ignore = self.extract_text(soup)
            if not ignore:
                # print("Part III - {:d}".format(os.getpid()))
                info_dict["website"] = current_website
                self.store_info(info_dict)
            # except AssertionError:
            #     print("Error!")

        if current_depth < self.depth:
            # print("Part II-BIS - {:d}".format(os.getpid()))
            # If crawl_depth is less that max_depth, append new websites.

            # print("Part III-BIS - {:d}".format(os.getpid()))
            # print(len(self.crawl_list))
            return self.extract_links(soup, current_depth)
            #self.crawl_list += extracted
            # print(len(self.crawl_list))
        return []



    def store_info(self, info_dict):
        date_dir = self.article_root_dir + "/" + info_dict["date"]
        os.makedirs(date_dir, exist_ok=True)

        sym_link_flag = False
        src_file = ""
        for author_name in info_dict["author_name"]:
            author_dir = date_dir + "/" + author_name
            os.makedirs(author_dir, exist_ok=True)

            file_name = author_dir + "/" + "_".join(info_dict["tickers"]) + ".json"
            if sym_link_flag:
                try:
                    os.symlink(src_file, file_name)
                except FileExistsError:
                    pass
            else:
                sym_link_flag = True
                src_file = os.getcwd() + file_name[1:]
                with open(file_name, "w") as outfile:
                    json.dump(info_dict, outfile, sort_keys=True)

    def extract_text(self):
        # Parses text from a website.
        raise NotImplementedError

    def extract_links(self):
        # Parses links from a website.
        raise NotImplementedError
