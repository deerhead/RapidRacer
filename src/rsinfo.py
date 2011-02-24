#!/usr/bin/env python
from RapidRacer import RSFile, HostError
from sys import argv

class UnknownException(Exception):
    def __init__(self,error):
        self.error = error

def get_status(url):
    rsfile = RSFile(url)

    if rsfile.get_status() == 0:
        return "["+rsfile.get_filename()+"]: File not found"
    elif rsfile.get_status() == 1:
        return "["+rsfile.get_filename()+"]: File OK (Anonymous downloading)"
    elif rsfile.get_status() == 3:
        return "["+rsfile.get_filename()+"]: Server down"
    elif rsfile.get_status() == 4:
        return "["+rsfile.get_filename()+"]: File marked as illegal"
    elif rsfile.get_status() == 5:
        return ("["+rsfile.get_filename()+"]: Anonymous file locked, "+ 
                "because it has more than 10 downloads already")
    elif rsfile.get_status() >= 50 and rsfile.get_status() < 100:
        return ("["+rsfile.get_filename()+"]: File OK (TrafficShare"+
                "direct download type "+str(rsfile.get_status()-50)+
                "without any logging.)")
    elif rsfile.get_status() >= 100:
        return ("["+rsfile.get_filename()+"]: File OK (TrafficShare "+
                " direct download type "+str(rsfile.get_status()-100)+
                " with logging. Read our privacy policy to see what "+
                "is logged.)")
    else:
        raise UnknownException("Unknown error occured")

if len(argv) < 2:
    print "Usage:",argv[0],"[first url], [second url]..."
    exit(1)

if __name__ == "__main__":
    for url in argv[1:]:
        try:
            print get_status(url),"\n"
        except UnknownException,e:
            print e.error,"while checking",url
        except HostError, h:
            print h.host,"doesn't seem to be a valid"
    
