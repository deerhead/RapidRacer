#!/usr/bin/env python

from optparse import OptionParser
from RapidRacer.get_rs_file_info import RSFile
from RapidRacer.link_finder import FilesTubeSearch, GoogleSearch, Finder
from RapidRacer.url_token_defines import *
import threading

class SearchAtGoogle(threading.Thread):
    
    def __init__(self,args):
        
        threading.Thread.__init__(self)
        self.__args = args
        self.__gsearch = GoogleSearch(self.__args)
        self.__checked_links = []
        
    def run(self):
    
        global link_dict
        
        nr = 0
        while True:
            
            for link in self.__gsearch.get_link_list():
                
                if link in self.__checked_links:
                    continue
                
                finder = Finder(link)
                rs_link_list = finder.get_rs_link_list()
                
                if len(rs_link_list):
                
                    link_dict.update({link:rs_link_list})
                
                if len(link_dict) == options.count:
                    return

            self.__gsearch.set_page_nr(nr)
            self.__gsearch.reload_page()
        
        
class SearchAtFilesTube(threading.Thread):
    
    def __init__(self,args):
        
        threading.Thread.__init__(self)
        self.__args = args
        self.__fssearch = FilesTubeSearch(self.__args,FT_SEARCH_RAPIDSHARE)
        self.__checked_links = []
        
    def run(self):
    
        global link_dict
        
        nr = 0
        
        while True:

            for link in self.__fssearch.get_link_list():
                
                if not "filestube" in link or link in self.__checked_links:
                    continue
                
                finder = Finder(link)
                rs_link_list = finder.get_rs_link_list()
                
                if len(rs_link_list):
                
                    link_dict.update({link:rs_link_list})
                    
                if len(link_dict) == options.count:
                    return
                
                self.__checked_links.append(link)
                
            self.__fssearch.set_page_nr(nr)
            self.__fssearch.reload_page()


if __name__ == "__main__":
    
    opt_parser = OptionParser()
    opt_parser.add_option("-g", "--google", dest="google",
                          help="Search at Google", action="store_true",
                          default="False")
    opt_parser.add_option("-f", "--filestube", dest="filestube",
                          help="Search at FilesTube", action="store_true",
                          default="False")
    opt_parser.add_option("-c", "--count", dest="count")
    
    ### Not implemented yet ###
#   opt_parser.add_option("-H", "--host", dest="host")

    opt_parser.set_usage("raprac [options] search keywords")

    (options, args) = opt_parser.parse_args()
    
    if len(args)<1:
        opt_parser.error("No keywords given.")
        
    if not options.google and not options.filestube:
        opt_parser.error("No search parameter given.")
        
    if not options.count:
        options.count = 1
    
    link_dict   = {}
    thread_dict = {}
    
    fs_search = SearchAtFilesTube(args)
    g_search = SearchAtGoogle(args)
    
    if options.filestube:
        
        thread_dict.update({"FilesTubeSearch":SearchAtFilesTube(args)})
        thread_dict["FilesTubeSearch"].start()
    
    if options.google:
        
        thread_dict.update({"GoogleSearch":SearchAtGoogle(args)})
        thread_dict["GoogleSearch"].start()
        
    print "Racing..."
    
    for key in thread_dict.keys():
        thread_dict[key].join()
    
    for site in link_dict.keys():
        print site
        for link in link_dict[site]:
            if (RSFile(link).get_status()==RS_FILE_OK or
                RSFile(link).get_status()==RS_FILE_OK_PLUS):
                print "\t|",link,"[ONLINE]"
            else:
                print "\t|",link,"[OFFLINE]"
            