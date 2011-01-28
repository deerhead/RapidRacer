# coding: utf8
from urllib import FancyURLopener
from url_token_defines import *
from get_rs_file_info import *
import re

class Finder():
	
	def __init__(self, url, ignored_cont=[]):
		
		self.__ignored_cont	= ignored_cont
		self.__url			= url
		self.__opener		= FancyURLopener()
		
		self.__setup_finder()
		
	def __setup_finder(self):
		
		self.__page			= self.__opener.open(self.__url)
		self.__content		= self.__page.read()
		self.__link_list	= self.__get_any_links_on_site(self.__ignored_cont)
		self.__rs_link_list	= self.__get_rs_links_on_site()
		
	def __get_page(self, url):
		
		self.__content = self.__opener.open(self.__url)

	def __get_any_links_on_site(self,ignored_cont=[]):
		
		if not self.__content:
			return 4

		link_list	= []
		tmp_list	= re.findall(r"http://\S*[\",\,]?"[0:-1],
								self.__content)

		for element in tmp_list:
			contains = 0
			for cont in ignored_cont:
				if cont in element:
					contains = 1
					break

			if not contains:
				link_list.append(element)
		
		return link_list
	
	def __get_rs_links_on_site(self):

		if not self.__content:
			return 4
		
		link_list = (re.findall(r"http://www.rapidshare.com[\w,/,\\,\.]*",self.__content)+
					 re.findall(r"http://rapidshare.com[\w,/,\\,\.]*"    ,self.__content))

		return link_list
	
	def get_link_list(self):
		
		return self.__link_list
	
	def get_rs_link_list(self):
		
		return self.__rs_link_list

class GoogleSearch(Finder):
	
	def __init__(self,keyword_list):
		
		self.__opener		= FancyURLopener()
		self.__page_nr 		= "0"
		self.__keyword_list	= keyword_list
		
		self.__gen_search_url()
		
		Finder.__init__(self, self.__url, ["google"])
		
	
	def __gen_search_url(self):
		
		tmp_url = (GOOGLE_URL + GOOGLE_SEARCH_KEYS(self.__keyword_list)
				 	+ AND + GOOGLE_SEARCH_PAGE(self.__page_nr))
		return tmp_url
	
	def load_page(self, page_nr):
		
		self.__page_nr = str(page_nr)
		self.__gen_search_url()
		self.__setup_finder(["google"])
	
	def load_keyords(self,keyword_list):
		
		self.__keyword_list = keyword_list
		self.__gen_search_url()
		self.__setup_finder(["google"])
	
class FilesTubeSearch(Finder):

	def __init__(self,keyword_list,host_list):


		self.__page_nr		= "1"
		self.__keyword_list	= keyword_list
		self.__host_list	= host_list
		
		self.__gen_search_url()
		
		Finder.__init__(self, self.__url)

	def __gen_search_url(self):
		
		"""
		Generiert eine Such-URL für FilesTube
		"""
		
		self.__url = (FT_URL+FT_SEARCH+
				   FT_SEARCH_KEYWORDS(self.__keyword_list)+AND+
				   FT_SEARCH_HOSTS(self.__host_list)+AND+
				   FT_SEARCH_PAGE(self.__page_nr))
	
	def __search_source_link(self):
		
		"""
		Sucht auf der Seite eines Einzelnen Suchergebnisses den
		Link zur Quelle, auf der der Link ursprünglich liegt
		"""
		
		pass
	
	def load_page(self,page_nr):
	
		"""
		Modifiziert die Such-URL, holt Content der (als Integer)
		übergebenen Seite.
		"""
		
		self.__page_nr = page_nr
		self.__gen_search_url(self.__keyword_list)
		Finder().__init__(self,self.__url)
		
	def load_keywords(self, keyword_list):
		
		"""
		Modifiziert die Such-URL, holt Content der neuen Suche.
		"""
		
		self.__keyword_list = keyword_list
		self.__gen_search_url(self.__keyword_list)
		Finder().__init__(self,self.__url)
	
	def load_hosts(self, host_list):
		
		"""
		Modifiziert die Such-URL, holt Content der Suche mit den
		neu angegebenen Hosts.
		"""
		
		self.__host_list = host_list
		self.__gen_search_url(self.__keyword_list)
		Finder().__init__(self,self.__url)
		
	def debug_get_url(self):
		
		print self.__url