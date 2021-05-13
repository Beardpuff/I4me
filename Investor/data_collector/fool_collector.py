# \todo(vrubies) Make script/class that load data from a website and
# saves info to the data folder.

from data_collector_main import WebsiteDataCollector

from bs4 import BeautifulSoup
from collections import OrderedDict
import bs4
import requests
import html2text as h2t
import unidecode
import re

# url = raw_input("Enter a website to extract the URL's from: ")
# r  = requests.get("http://" +url)
# data = r.text
# soup = BeautifulSoup(data)
# for link in soup.find_all('a'):
#     print(link.get('href'))


class FoolCollector(WebsiteDataCollector):

    def __init__(self, name, website, range_idx, initial_has_info=False, initial_address=None):
        if initial_address is not None:
            assert isinstance(initial_address, list)
        else:
            initial_address = [
                "https://www.fool.com/investing-news/?page={:d}".format(
                ii) for ii in range_idx]
        super(FoolCollector, self).__init__(name, website, initial_address)

        self.initial_has_info = initial_has_info
        self.parse_links_rules = {
            "links":        [("div", {"class": "list-content"}),
                             ("a",   {"href": True}),
                             ]}
        self.parse_text_rules = {
            "author_name":  [("div", {"class": "author-name"}),
                             ("a",    {})
                             ],
            "date":         [("div", {"class": "publication-date"})
                             ],
            "tickers":      [("span", {"class": "article-content"}),
                             ("p",    {}),
                             ("span", {"class": "ticker"}),
                             ("a",    {})
                             ],
            "article_text": [("span", {"class": "article-content"}),
                             ("p",    {})
                             ]}

        self.month_dict = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04",
                           "May":"05", "Jun":"06", "Jul":"07", "Aug":"08",
                           "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}

        super(FoolCollector, self).check_ready()

    def extract_links(self, soup, depth):
        # Link extractor for Motley Fool.
        web_links = []

        parse_rules = self.parse_links_rules.copy()
        for key in parse_rules:
            info = []
            self.rule_popper([soup], parse_rules[key], info)

            if key is "links":
                for soup_element in info:
                    next_website = self.website + soup_element['href']
                    has_info = True
                    web_links.append((next_website, has_info, depth+1))

        return web_links

    def extract_text(self, soup):
        # Text extractor for Motley Fool.
        all_info = OrderedDict()

        h = h2t.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        parse_rules = self.parse_text_rules.copy()
        for key in parse_rules:
            info = []
            self.rule_popper([soup], parse_rules[key], info)

            if key is "author_name":
                author_name = []
                for name in info:
                    name_text = self.clean_author(h.handle(str(name)))
                    for single_author in name_text.split(","):
                        author_name.append(single_author)
                all_info[key] = author_name
            if key is "date":
                date_text = h.handle(str(info[0]))
                date_text = self.clean_text(date_text).replace(
                    " ", "_").replace(":", "-").replace(",", "")
                date_elements = date_text.split("_")[:3]
                assert date_elements[0] in self.month_dict.keys()
                date_elements[0] = self.month_dict[date_elements[0]]
                date_elements.insert(0, date_elements.pop())
                all_info[key] = "_".join(date_elements)
            if key is "article_text":
                article_text = ""
                for paragraph in info:
                    paragraph_text = h.handle(str(paragraph))
                    article_text += self.clean_text(paragraph_text) + " "
                article_text = ' '.join(article_text.split())
                all_info[key] = article_text
            if key is "tickers":
                tickers = []
                for ticker in info:
                    ticker_text = self.clean_text(h.handle(str(ticker)))
                    ticker_text = ":".join([re.sub(r'\W+', '', tt) for tt in ticker_text.split(":")])
                    tickers.append(ticker_text)
                all_info[key] = tickers

        return all_info

    def clean_author(self, text):
        new_text = text.replace("and", ",").replace("And", ",").replace(
                                "CFP", "").replace("CFA", "").replace(
                                "PhD", "").replace("CPA", "")
        new_text = self.clean_text(new_text)
        new_text = new_text.replace(" , ", ",")
        new_text = new_text.replace(" ,", ",")
        new_text = new_text.replace(", ", ",")
        while ",," in new_text:
            new_text = new_text.replace(",,", ",")
        if new_text[-1] == ",":
            new_text = new_text[:-1]
        new_text = new_text.replace(" ", "_")
        # new_text = new_text.replace("_,_", "")
        # new_text = new_text.replace(",_", ",")
        # new_text = new_text.replace("_,", "")
        return new_text

    def clean_text(self, text):
        return unidecode.unidecode(' '.join(
            (text.replace("\n", " ").replace("*", " ").replace(
             "\\", " ").replace("-", " ")).split()))

    def rule_popper(self, soup, parse_rules, info):
        # Pops out the list of rules one at a time.
        if len(parse_rules) > 0:
            assert isinstance(soup, list)
            for soup_element in soup:
                tag_name, attribute = parse_rules[0]
                sub_soup = soup_element.find_all(tag_name, attribute)
                self.rule_popper(sub_soup, parse_rules[1:], info)
        else:
            info += soup

    # def List_maker(self,
    #                parse_rules,
    #                soup_list,
    #                web_list):
    #     # Parses the list of links in Motley Fool.

    #     if(len(parse_rules) > 0):
    #         # If there is more info to extract.
    #         current_parse = parse_rules[depth]
    #         tag_name, attribute = current_parse
    #         for soup_element in soup_list:
    #             new_soup = soup_element.find_all(tag_name, attribute)
    #             self.List_maker(parse_rules[1:], new_soup, web_list)
    #     else:
    #         for soup_element in soup_list:
    #             web_list.append(soup_element['href'])

    # # \todo(vrubies) finish article parser.
    # def Article_parser(self,
    #                    parse_rules,
    #                    soup_list,
    #                    depth,
    #                    article_text,
    #                    article_tickers):
    #     # Parses an article from the Motley Fool.
    #     if(len(parse_rules) > 0):
    #         # If there is more info to extract.
    #         current_parse = parse_rules[depth]
    #         tag_name, attribute = current_parse
    #         for soup_element in soup_list:
    #             self.Article_parser(parse_rules, new_soup, depth+1,
    #                                 article_text, article_tickers)
    #     else:
    #         s = soup_list[0]
    #         article_list.append(s['href'])

    # def crawl(self,
    #           depth=0,
    #           verbose=False):
    #     # Crawler: It will loop thorugh Motley Fool's
    #     # articles and extract article text and tickers.

    #     parse_rules = [("div", {"class": "list-content"}),
    #                    ("a",   {"href": True}),
    #                    # ("div", {"class": "text"}),
    #                    # ("h4",  {}),
    #                    # ("a",   {})
    #                    ]
    #     article_rules = [("span", {"class": "article-content"}),
    #                      ("p",    {}),
    #                      ("a",    {})
    #                      ]

    #     data = requests.get(self.initial_address).text

    #     # For loop
    #     soup_list = [BeautifulSoup(data, 'html.parser')]
    #     web_list = []

    #     for

    #     self.List_maker(parse_rules, soup_list, web_list)
    #     if(verbose):
    #         for web in web_list:
    #             print(web)

    #     article_list = []
    #     for web in web_list:
    #         current_web = self.website+web
    #         article_data = requests.get(current_web).text
    #         soup_list = [BeautifulSoup(article_data, 'html.parser')]
    #         text = []
    #         tickers = []
    #         self.Article_parser(article_rules, soup_list, text, tickers)
