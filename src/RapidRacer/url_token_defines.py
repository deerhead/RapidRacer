# coding: utf8

AND = "&"
REGEXP_URL = r"[\w,\-,+,\\,/,&,=,.,?,(,)]*"

#### FilesTube ####
FT_URL = "http://www.filestube.com/"

FT_SEARCH = "search.html?"
FT_SEARCH_RAPIDSHARE    = "1"
FT_SEARCH_MEGAUPLOAD    = "3"
FT_SEARCH_UPLOADED      = "24"
FT_SEARCH_HOTFILE       = "27"

FT_SEARCH_PAGE = lambda page: "page=" + str(page)

def FT_SEARCH_FILETYPE(filetype_list):

    host_var = "select="
    for host in filetype_list:
        host_var = host_var + host + ","
    return host_var[0:-1]

def FT_SEARCH_HOSTS(host_list):

    host_var = "hosting="
    for host in host_list:
        host_var = host_var + host + ","
    return host_var[0:-1]


def FT_SEARCH_KEYWORDS(keyword_list):
    
    search_var = "q="
    for keyword in keyword_list:
        search_var = search_var + keyword + "+"
    return search_var[0:-1]
###################

#### Rapidshare API ####
RS_API_URL          = "http://api.rapidshare.com/cgi-bin/rsapi.cgi?"
RS_API_CHECK_FILES  = "sub=checkfiles&files=" 
RS_API_ADD_FILE     = lambda file_id, filename: file_id + "&" + "filenames=" + filename
RS_FILE_OK          = 1
RS_FILE_NOT_FOUND   = 0
RS_FILE_OK_PLUS     = 50
########################

#### Google Search ####
GOOGLE_URL = "http://www.google.com/search?"
GOOGLE_SEARCH_PAGE = lambda page_nr: "start=" + page_nr


def GOOGLE_SEARCH_KEYS(keyword_list):
    
    search_var = "q="
    for keyword in keyword_list:
        search_var = search_var + keyword + "+"
    return search_var[0:-1]
#######################