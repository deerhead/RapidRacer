# coding: utf8
from urllib import FancyURLopener
from url_token_defines import *
from get_rs_file_info import *
import re


class Finder():
    
    def __init__(self, url, ignored_cont=[]):
        
        self.__ignored_cont = ignored_cont
        self.__opener = FancyURLopener()
        self.__opener.addheader("User-Agent",
                                "Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11")
        self.__setup_finder(url)
        
    def __setup_finder(self,url):
        
        self.__url = url
        self.__page = self.__opener.open(self.__url)
        self.__content = self.__page.read()
        self.__link_list = self.__get_any_links_on_site(self.__ignored_cont)
        self.__rs_link_list = self.__get_rs_links_on_site()
        
    def __get_page(self, url):
        
        self.__content = self.__opener.open(self.__url)

    def __get_any_links_on_site(self, ignored_cont=[]):
        
        # Return 4 if self.__content is empty
        if not self.__content:
            return 4

        # Define some used variables
        link_list = []
        tmp_list = re.findall(r"http://" + REGEXP_URL,
                                self.__content)

        for element in tmp_list:
            
            contains = 0
            # Search for unwanted keywords in every URL in the list
            for cont in ignored_cont:
                if cont in element:
                    contains = 1
                    break
            # If no unwanted keywords were found, append the element to
            # the link_list
            if not contains:
                link_list.append(element)
        
        return link_list
    
    def __get_rs_links_on_site(self):

        # Get page content and search everything, that looks like a
        # rapidshare link via regexp
        if not self.__content:
            return 4
        
        link_list = (re.findall(r"http://www.rapidshare.com" + REGEXP_URL, self.__content) + 
                     re.findall(r"http://rapidshare.com" + REGEXP_URL    , self.__content))

        return link_list
    
    def get_link_list(self):
        
        return self.__link_list
    
    def get_rs_link_list(self):
        
        return self.__rs_link_list
    
    def get_content(self):
        
        return self.__content
    
    def get_ignored_content(self):
        
        return self.__ignored_cont
    
    def get_url(self):
        
        return self.__url


class GoogleSearch(Finder):
    
    def __init__(self, keyword_list):
        
        self.__page_nr = "0"
        self.__keyword_list = keyword_list
        
        Finder.__init__(self, self.__gen_search_url(), ["google"])
        
    def __gen_search_url(self):
        
        tmp_url = (GOOGLE_URL + GOOGLE_SEARCH_KEYS(self.__keyword_list)
                     + AND + GOOGLE_SEARCH_PAGE(self.__page_nr))
        return tmp_url
    
    def load_page_nr(self, page_nr):
        
        if type(page_nr) == str:
            raise TypeError("load_page_nr takes an integer as argument")
            
        self.__page_nr = str(page_nr)
        Finder.__init__(self, self.__gen_search_url(), ["google"])
    
    def load_keyords(self, keyword_list):
        
        if type(keyword_list) == list:
            raise TypeError("load_keywords takes a list as argument")
            
        self.__keyword_list = keyword_list
        Finder.__init__(self, self.__gen_search_url(), ["google"])
    

class FilesTubeSearch(Finder):

    def __init__(self, keyword_list, host_list):


        self.__page_nr = "1"
        self.__keyword_list = keyword_list
        self.__host_list = host_list
        
        Finder.__init__(self, self.__gen_search_url())
        
    def __gen_search_url(self):
        
        """
        Generiert eine Such-URL für FilesTube
        """
        
        tmp_url = (FT_URL + FT_SEARCH + 
                   FT_SEARCH_KEYWORDS(self.__keyword_list) + AND + 
                   FT_SEARCH_HOSTS(self.__host_list) + AND + 
                   FT_SEARCH_PAGE(self.__page_nr))
        return tmp_url
        
    def __search_source_link(self):
        
        """
        Sucht auf der Seite eines Einzelnen Suchergebnisses den
        Link zur Quelle, auf der der Link ursprünglich liegt
        """
        
        pass
    
    def load_page_nr(self, page_nr):
        
        if type(page_nr) == str:
            raise TypeError("load_page_nr takes an integer as argument")
            
        self.__page_nr = str(page_nr)
        Finder.__init__(self, self.__gen_search_url(), ["google"])
    
    def load_keyords(self, keyword_list):
        
        if type(keyword_list) == list:
            raise TypeError("load_keywords takes a list as argument")
            
        self.__keyword_list = keyword_list
        Finder.__init__(self, self.__gen_search_url())
    
    def load_hosts(self, host_list):
        
        """
        Modifiziert die Such-URL, holt Content der Suche mit den
        neu angegebenen Hosts.
        """
        
        if type(host_list) == list:
            raise TypeError("load_hosts takes a list as argument")
            
        self.__host_list = host_list
        Finder.__init__(self, self.__gen_search_url())
        
    def debug_get_url(self):
        
        print self.__url
