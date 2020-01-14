# \todo(vrubies) Make script/class that load data from a website and
# saves info to the data folder.

from bs4 import BeautifulSoup
import requests

# url = raw_input("Enter a website to extract the URL's from: ")
# r  = requests.get("http://" +url)
# data = r.text
# soup = BeautifulSoup(data)
# for link in soup.find_all('a'):
#     print(link.get('href'))

class WebsiteDataCollector():

	def __init__(self,
							 name,
							 website,
							 initial_address):

		self.name = name
		self.website = website
		self.initial_address = initial_address

	def crawl(self,
						verbose=False):

		list_rules = \
						[("div",		{"class"	,		"list-content"		}),
						 ("div", 		{"class"	,		"text"						}),
						 ("h4" ,		{}															 ),
						 ("a",			{}															 )
						 ]
		article_rules = \
						[("span",		{"class"	,		"article-content"		}),
						 ("p", 			{}																 ),
						 ("a" ,			{}															 	 )
						 ]

		data = requests.get(self.initial_address).text
		
		#For loop
		soup_list = [BeautifulSoup(data,'html.parser')]
		web_list = []
		
		self.List_maker(list_rules,soup_list,0,web_list)
		if(verbose):
			for web in web_list:
				print(web)

		article_list = [];
		for web in web_list:
			current_web = self.website+web;
			article_data = requests.get(current_web).text
			soup_list = [BeautifulSoup(article_data,'html.parser')]
			text = []
			tickers = []
			self.Article_parser(article_rules,soup_list,0,text,tickers);



	def List_maker(self,
							   rules,
				  			 soup_list,
				  			 depth,
				  			 web_list):

		if(len(rules) > depth):
			r_now = rules[depth]
			r1,r2 = r_now
			for s in soup_list:
				new_soup = s.findAll(r1,r2)
				self.List_maker(rules,new_soup,depth+1,web_list)
		else:
			s = soup_list[0]
			web_list.append(s['href'])

	# \todo(vrubies) finish article parser.
	def Article_parser(self,
										 rules,
										 soup_list,
										 depth,
										 text,
										 tickers):
		if(depth == 1):
			s = soup_list[0]
			text.append(s.text)
		if(depth == 2):
			s = soup_list[0]
			tickers.append(s.text)
		if(len(rules) > depth):
			r_now = rules[depth]
			r1,r2 = r_now
			for s in soup_list:
				new_soup = s.findAll(r1,r2)
				self.Article_parser(rules,new_soup,depth+1,article_list)
		else:
			s = soup_list[0]
			article_list.append(s['href'])		

