#!/usr/bin/env python

from optparse import OptionParser
from RapidRacer import *
import threading
from time import sleep

def check_for_rs_links(link):

    # Search for rapidshare links, add them to the link
    # dictionary and returns '2' if there are enough links
    # collected.
    try:
        finder     = Finder(link)
    except IOError:
        if options.debug:
            print "[*] Error while checking",link
        return 1

    if      (options.host == "rapidshare" or
             options.host == "rs"):
        link_list   = finder.get_rs_link_list()
    elif    (options.host == "megaupload" or
             options.host == "mu"):
        link_list   = finder.get_mu_link_list()
    elif    (options.host == "hotfile" or
             options.host == "hf"):
        link_list   = finder.get_hf_link_list()
    elif    (options.host == "uploaded" or
             options.host == "uploaded"):
        link_list   = finder.get_ul_link_list()
    else:
        print "Unknown one-click-hoster given"
        exit(4)

    if len(link_list):
        link_dict.update({link:link_list})
        if options.debug:
            print "[%i]"%len(link_dict),link
            for ln in link_list:
                print "\t'-> "+ln
    if len(link_dict) == int(options.count):
        return 2

class SearchAtFilesTube(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)

        self.__checked_links = []

        try:
            self.__ftsearch = FilesTubeSearch(args,[options.host],
                                              [options.filetype])
        # If the given one-click-hoster isn't known, the link_finder
        # will raise a HostError exception
        except HostError,host:
            print "The given host %s is not a known one-click-hoster"%host
            exit(2)
        except FiletypeError, filetype:
            print "The given Filetype %s is not a known filetype"%filetype
            exit(3)

    def run(self):

        global link_dict

        self.__nr=1
        while True:
            for link in self.__ftsearch.get_link_list():

                if not "filestube" in link:
                    continue
                # Manage and check the self.__checked_links-list
                if link in self.__checked_links:
                    continue
                self.__checked_links.append(link)

                #
                do = check_for_rs_links(link)
                if do == 1:
                    continue
                elif do == 2:
                    return
            # If there are less than 150 links at the site, return
            if len(self.__ftsearch.get_link_list())<150:
                return
            # Load the next page from the filestube search
            self.__nr+=1
            self.__ftsearch.set_page_nr(self.__nr)
            self.__ftsearch.reload_finder()


class SearchAtGoogle(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)

        self.__checked_links = []
        try:

            self.__gsearch = GoogleSearch(args,[options.host])

        # If the given one-click-hoster isn't known, the link_finder
        # will raise a HostError exception
        except HostError,host:
            print "The given host %s is not a known one-click-hoster"%host

        self.__checked_links = []

    def run(self):

        global link_dict

        self.__nr=1
        while True:
            for link in self.__gsearch.get_link_list():
                # Manage and check the self.__checked_links-list
                if link in self.__checked_links:
                    continue
                self.__checked_links.append(link)

                do = check_for_rs_links(link)
                if do == 1:
                    continue
                elif do == 2:
                    return
            # If there are less than 150 links at the site, return
            if len(self.__gsearch.get_link_list())<30:
                return
            # Load the next page from the filestube search
            self.__nr+=1
            self.__gsearch.set_page_nr(self.__nr)
            self.__gsearch.reload_finder()


if __name__ == "__main__":

    ### Set up the OptionParser
    opt_parser = OptionParser("raprac [options] search keywords")
    opt_parser.add_option("-g", "--google", dest="google",
                          help="Search at Google", action="store_true",
                          default=False)
    opt_parser.add_option("-f", "--filestube", dest="filestube",
                          help="Search at FilesTube", action="store_true",
                          default=False)
    opt_parser.add_option("-d", "--debug", dest="debug",
                          help="Debugging mode", action="store_true",
                          default=False)
    opt_parser.add_option("-c", "--count", dest="count")
    opt_parser.add_option("-t", "--filetype", dest="filetype")
    opt_parser.add_option("-H", "--host", dest="host")

    (options, args) = opt_parser.parse_args()
    ###

    # Check the given parameters and arguments
    if len(args)<1:
        opt_parser.error("No keywords given.")

    if not options.google and not options.filestube:
        opt_parser.error("No search machine defined")

    if not options.count:
        options.count = 1

    # Set a search for rapidshare links and all file type as default
    if not options.host:
        options.host = "rapidshare"

    if not options.filetype:
        options.filetype = "all"

    # Declaration of some important dictionaries
    link_dict   = {}
    thread_dict = {}
    link_list	= []

    # Run the filestube search if the parameter was set
    if options.filestube:
        thread_dict.update({"FilesTubeSearch":SearchAtFilesTube()})
        thread_dict["FilesTubeSearch"].start()
        if options.debug:
            print "[*] Searching at FilesTube"
    # Run the google search if the parameter is set
    if options.google:
        thread_dict.update({"GoogleSearch":SearchAtGoogle()})
        thread_dict["GoogleSearch"].start()
        if options.debug:
            print "[*] Searching at Google"

    print "Racing..."

    # Wait until the threads have finished
    for key in thread_dict.keys():
        thread_dict[key].join()
    # For readability in debugger mode
    if options.debug:
        print 2*"\n"
    # Checks the status of the found rapidshare links
    nr = 1
    for site in link_dict.keys():
        print "\n["+str(nr)+"]",site
        sleep(0.5)
        if options.host == "rapidshare":
            for link in link_dict[site]:
                try:
                    if (RSFile(link).get_status()==RS_FILE_OK or
                        RSFile(link).get_status()==RS_FILE_OK_PLUS):
                        print " |[ONLINE]\t",link
                    else:
                        print " |[OFFLINE]\t",link
                except SyntaxError:
                    print " |[STATUS UNCHECKED]\t",link
        else:
            for link in link_dict[site]:
                print " |",link
        nr+=1