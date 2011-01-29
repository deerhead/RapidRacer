# coding: utf8
from urllib import FancyURLopener
from url_token_defines import *
from get_rs_file_info import *
import re


class Finder():
    
    """
    Describes a website and searches for normal links and rapidshare links
    on that site.
    """
    
    def __init__(self, url, ignored_cont=[]):
        
        # configure the FancyURLopener
        self.__ignored_cont = ignored_cont
        self.__opener = FancyURLopener()
        self.__opener.addheader("User-Agent",
                                "Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11")
        
        self.__setup_finder(url)
        
    def __setup_finder(self,url):
        
        # defines some essential variables
        self.__url = url
        self.__page = self.__opener.open(self.__url)
        self.__content = self.__page.read()
        self.__link_list = self.__get_any_links_on_site(self.__ignored_cont)
        self.__rs_link_list = self.__get_rs_links_on_site()

    def __get_any_links_on_site(self, ignored_cont=[]):

        # Empty link_list will be used to append some URLs
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
        link_list = (re.findall(r"http://www.rapidshare.com" + REGEXP_URL, self.__content) + 
                     re.findall(r"http://rapidshare.com" + REGEXP_URL    , self.__content))

        return link_list
    
    def get_link_list(self):
        
        """
        Returns a list of all links at the current site except the links
        they contain an unwanted word.
        """
        
        return self.__link_list
    
    def get_rs_link_list(self):
        
        """
        Returns all links at the current site they look like a Rapidshare
        link.
        """
        
        return self.__rs_link_list
    
    def get_ignored_content(self):
        
        """
        Returns the given list of ignored words.
        """
        
        return self.__ignored_cont
    
    def get_url(self):
        
        """
        Returns the currently set URL
        """
        
        return self.__url
    
    def set_ignored_cont(self,ignored_cont):
        
        """
        Sets a new list with ignored words and overwrites the old one
        """
        
        self.__ignored_cont = ignored_cont
        
    def reload_page(self):
        
        """
        Reloads the current page.
        """
        
        self.__setup_finder(self.__url)


class GoogleSearch(Finder):
    
    """
    Describes a search at Google.com. Inherits form 'Finder' 
    """
    
    def __init__(self, keyword_list):
        
        # Set some essential variables
        self.__page_nr = "0"
        self.__keyword_list = keyword_list
        
        Finder.__init__(self, self.__gen_search_url(), ["google"])
        
    def __gen_search_url(self):
        
        # Generates a valid Google search URL
        tmp_url = (GOOGLE_URL + GOOGLE_SEARCH_KEYS(self.__keyword_list)
                     + AND + GOOGLE_SEARCH_PAGE(self.__page_nr))
        return tmp_url
    
    def set_page_nr(self, page_nr):
        
        """
        Sets the new page number and overwrites the old one.
        """
        
        # Checks if page_nr is an instance from 'list'
        if type(page_nr) == str:
            raise TypeError("load_page_nr takes an integer as argument")
            
        self.__page_nr = str(page_nr)
    
    def set_keyords(self, keyword_list):
        
        """
        Sets a new list of words to search for and overwrites the old one.
        """
        
        # Checks if page_nr is an instance from 'list'
        if type(keyword_list) == list:
            raise TypeError("load_keywords takes a list as argument")
            
        self.__keyword_list = keyword_list
    

class FilesTubeSearch(Finder):

    """
    Describes a search at FilesTube.com. Inherits from 'Finder'
    """
    
    def __init__(self, keyword_list, host_list):

        self.__page_nr = "1"
        self.__keyword_list = keyword_list
        self.__host_list = host_list
        
        Finder.__init__(self, self.__gen_search_url())
        
    def __gen_search_url(self):
        
        # Generates a valid FilesTube search URL
        tmp_url = (FT_URL + FT_SEARCH + 
                   FT_SEARCH_KEYWORDS(self.__keyword_list) + AND + 
                   FT_SEARCH_HOSTS(self.__host_list) + AND + 
                   FT_SEARCH_PAGE(self.__page_nr))
        return tmp_url
    
    def set_page_nr(self, page_nr):
        
        """
        Sets the new page number and overwrites the old one
        """
        if type(page_nr) == str:
            raise TypeError("load_page_nr takes an integer as argument")
            
        self.__page_nr = str(page_nr)
    
    def set_keyords(self, keyword_list):
        
        """
        Sets a new list of words to search for and overwrites the old one.
        """
        
        if type(keyword_list) == list:
            raise TypeError("load_keywords takes a list as argument")
            
        self.__keyword_list = keyword_list
    
    def set_hosts(self, host_list):
        
        """
        Sets a new list of one-click-hosters and overwrites the old one.
        """
        
        if type(host_list) == list:
            raise TypeError("load_hosts takes a list as argument")
            
        self.__host_list = host_list