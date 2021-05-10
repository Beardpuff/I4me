# \todo(vrubies) Make script/class that load data from a website and
# saves info to the data folder.

from data_collector_main import WebsiteDataCollector

from bs4 import BeautifulSoup
import requests
import html2text as h2t

# url = raw_input("Enter a website to extract the URL's from: ")
# r  = requests.get("http://" +url)
# data = r.text
# soup = BeautifulSoup(data)
# for link in soup.find_all('a'):
#     print(link.get('href'))


class FoolCollector(WebsiteDataCollector):

    def __init__(self,
                 name,
                 website,
                 initial_address):
        super(FoolCollector, self).__init__(name, website, initial_address)

        self.initial_has_info = False
        self.parse_links_rules = {
            "links":        [("div", {"class": "list-content"}),
                             ("a",   {"href": True}),
                             ]}
        self.parse_text_rules = {
            "author_name":  [("span", {"class": "article-content"}),
                             ("p",    {}),
                             ("a",    {})
                             ],
            "article_text": [("span", {"class": "article-content"}),
                             ("p",    {}),
                             ("a",    {})
                             ]}

        super(FoolCollector, self).check_ready()

    def extract_links(self, soup, depth):
        # Link extractor for Motley Fool.
        web_links = []

        parse_rules = self.parse_links_rules.copy()
        for key in parse_rules:
            sub_soup = self.rule_popper(soup.copy(), parse_rules[key])

            if key is "links":
                for soup_element in sub_soup:
                    next_website = self.website + soup_element['href']
                    has_info = True
                    web_links.append((next_website, has_info, depth+1))

        return web_links

    def extract_text(self, soup):
        # Text extractor for Motley Fool.

        parse_rules = self.parse_text_rules.copy()
        for key in parse_rules:
            sub_soup = self.rule_popper(soup.copy(), parse_rules[key])

            if key is "author_name":

            if key is "article_text":

        web_text = h2t.
        return web_text

    def rule_popper(self, soup, parse_rules):
        # Pops out the list of rules one at a time.
        while len(parse_rules) > 0:
            current_parse = parse_rules.pop(0)
            tag_name, attribute = current_parse
            soup = soup.find_all(tag_name, attribute)
        return soup

    def List_maker(self,
                   parse_rules,
                   soup_list,
                   web_list):
        # Parses the list of links in Motley Fool.

        if(len(parse_rules) > 0):
            # If there is more info to extract.
            current_parse = parse_rules[depth]
            tag_name, attribute = current_parse
            for soup_element in soup_list:
                new_soup = soup_element.find_all(tag_name, attribute)
                self.List_maker(parse_rules[1:], new_soup, web_list)
        else:
            for soup_element in soup_list:
                web_list.append(soup_element['href'])

    # \todo(vrubies) finish article parser.
    def Article_parser(self,
                       parse_rules,
                       soup_list,
                       depth,
                       article_text,
                       article_tickers):
        # Parses an article from the Motley Fool.
        if(len(parse_rules) > 0):
            # If there is more info to extract.
            current_parse = parse_rules[depth]
            tag_name, attribute = current_parse
            for soup_element in soup_list:
                self.Article_parser(parse_rules, new_soup, depth+1,
                                    article_text, article_tickers)
        else:
            s = soup_list[0]
            article_list.append(s['href'])

    def crawl(self,
              depth=0,
              verbose=False):
        # Crawler: It will loop thorugh Motley Fool's
        # articles and extract article text and tickers.

        parse_rules = [("div", {"class": "list-content"}),
                       ("a",   {"href": True}),
                       # ("div", {"class": "text"}),
                       # ("h4",  {}),
                       # ("a",   {})
                       ]
        article_rules = [("span", {"class": "article-content"}),
                         ("p",    {}),
                         ("a",    {})
                         ]

        data = requests.get(self.initial_address).text

        # For loop
        soup_list = [BeautifulSoup(data, 'html.parser')]
        web_list = []

        for

        self.List_maker(parse_rules, soup_list, web_list)
        if(verbose):
            for web in web_list:
                print(web)

        article_list = []
        for web in web_list:
            current_web = self.website+web
            article_data = requests.get(current_web).text
            soup_list = [BeautifulSoup(article_data, 'html.parser')]
            text = []
            tickers = []
            self.Article_parser(article_rules, soup_list, text, tickers)
