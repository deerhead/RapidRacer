from RapidRacer import get_rs_file_info, link_finder
from RapidRacer.url_token_defines import *

if __name__ == "__main__":
    file1 = get_rs_file_info.RSFile("http://rapidshare.com/files/120453782/2002")
    print file1.get_status()
    file1.reset_url("http://rapidshare.com/files/305232527/BatyasSeele.part1.rar.html")
    print file1.get_status()
    
    ### Doesnt work, don't know why... ###
    search3 = link_finder.GoogleSearch(["the","acacia","strain","rapidshare"])
    print search3.get_link_list()
    for url in search3.get_link_list():
        try:
            print url
            search4 = link_finder.Finder(url)
            print search4.get_rs_link_list()
        except:
            continue
           
#    search1 = link_finder.FilesTubeSearch(["the", "acacia", "strain"],
#                                         [FT_SEARCH_RAPIDSHARE])
#    print search1.get_link_list()
#    print search1.get_rs_link_list()
#    search1.debug_get_url()

#    for url in search1.get_link_list():
#        if not "filestube" in url:
#            continue
#        try:
#            print url
#            search2 = link_finder.Finder(url)
#            print search2.get_rs_link_list()
#        except:
#            continue