# coding: utf8
from urllib import FancyURLopener
from url_token_defines import *


class RSFile():
    
    """
    Describes a file, hosted on rapidshare
    """
    
    def __init__(self, url):
        
        self.__opener = FancyURLopener()
        self.__url_parsed = []
        
        self.__parse_url(url)
        self.__check_url()

        # Detect filename and file ID                                                                                     ###
        self.__filename = self.__url_parsed[-1]
        self.__file_id = self.__url_parsed[-2]
    
        ### Holt Daten anhand der zuvor definierten URL und speichert sie in den ###
        ### betreffenden Variablen                                                                          ###
        self.__get_info()

    def __parse_url(self,url):
        
        #Parses the given URL and defines the url_parsed attribute
        for p in url.split("/"):
            if len(p):
                self.__url_parsed.append(p)
    
    def __frame_info_url(self, file_id, filename):
        
        #Frames a rapidshare URL
        return RS_API_URL + RS_API_CHECK_FILES + RS_API_ADD_FILE(file_id, filename)
        
    def __check_url(self):

        #Checks if the given link is a valid rapidshare-URL
        
        if len(self.__url_parsed) < 5:
            raise SyntaxError("Scheint kein Rapidshare-Link zu sein")
        if (self.__url_parsed[1] != "rapidshare.com" and
            self.__url_parsed[1] != "www.rapidshare.com"):
            raise SyntaxError("Scheint kein Rapidshare-Link zu sein")

    def __get_info(self):

        # Gets the informations and defines the matching variables
        
        answer = self.__opener.open(
        self.__frame_info_url(self.__file_id, self.__filename))
        
        (self.__file_id, self.__filename, self.__size, self.__server_id,
         self.__status, self.__short_host, self.__md5) = answer.read().split(",")

    def reset_url(self, url):
        
        """
        Calls self.__init__ again
        """
        
        self.__init__(url)

        
    def get_status(self):
        
        """
        Returns the file status. The section about the file status from
        rapidshare API documentation:
        
        ''5:Status integer, which can have the following numeric values:
            0    = File not found
            1    = File OK (Anonymous downloading)
            3    = Server down
            4    = File marked as illegal
            5    = Anonymous file locked, because it has more than 10 downloads
                   already
            50+n = File OK (TrafficShare direct download type "n" without any logging.)
            100+n = File OK (TrafficShare direct download type "n" with logging. 
                           Read our privacy policy to see what is logged.)''

        """
        
        return int(self.__status)
