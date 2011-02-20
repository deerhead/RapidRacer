#!/usr/bin/env python

import Tkinter
from RapidRacer import *
import webbrowser
import threading
import tkMessageBox

class Search(threading.Thread):
    
    def __init__(self):
        app.check = False
        threading.Thread.__init__(self)
    def run(self):
        app.link_box.delete(0, app.link_box.size())
        if app.search.get() == "FilesTube":
            app.searchFilesTube()
            
        elif app.search.get() == "Google":
            app.searchGoogle()
        app.label5["text"] = ""
        return
    
class Info(Tkinter.Frame):
    def __init__(self,master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.Label = Tkinter.Label(self)
        self.Label["text"] = "Happy Birthday!"
        self.Label.pack(padx=23,pady=5)
        
class ShowLinks(Tkinter.Frame):
    
    def __init__(self,rs_link_list,master=None):
        Tkinter.Frame.__init__(self,master)
        self.pack()
        self.link_box = Tkinter.Listbox(self)
        self.link_box.pack(pady=5, padx=5,side="top",fill="both",expand=True)
        self.link_box.insert("end", *rs_link_list)
        self.link_box.bind("<<ListboxSelect>>", self.selectionChanged)
        
        self.infoLabel = Tkinter.Label(self)
        self.infoLabel.pack(side="bottom",pady=10)
        self.infoLabel["text"] = " "
        
        self.openButton = Tkinter.Button(self)
        self.openButton.pack(side="bottom",padx=200,pady=5,ipadx=50)
        self.openButton["text"] = "Open"
        self.openButton["command"] = self.__open_in_browser
    
    def selectionChanged(self,event):
        rs_file = RSFile(self.link_box.get(self.link_box.curselection()))
        if (rs_file.get_status() == 0 or
            rs_file.get_status() == 3 or
            rs_file.get_status() == 4 or
            rs_file.get_status() == 5):
            self.infoLabel["text"] = "Status: Offline"
        else:
            self.infoLabel["text"] = "Status: Online"
            
    def __open_in_browser(self):
        index = self.link_box.curselection()
        if index:
            webbrowser.open(self.link_box.get(index))
            
    
class Raprac(Tkinter.Frame):
    
    def __init__(self,master=None):

        Tkinter.Frame.__init__(self,master)
        self.menuBar = Tkinter.Menu(self)
        master.config(menu=self.menuBar)
        self.__fillMenuBar()
        self.pack()
        self.__create_widgets()
        
    def __create_widgets(self):
        
        self.cv = Tkinter.Canvas(self, width=471, height=100)
        self.cv.pack()
        
        self.img = Tkinter.PhotoImage(file="/home/tav/bin/logo.gif")
        self.cv.create_image(0,0, image=self.img, anchor="nw")
        
        self.label1 = Tkinter.Label(self)
        self.label1.pack(pady=12, padx=5)
        self.label1["text"] = "Welcome to raprac 0.17!"
        
        self.configContainer=Tkinter.Frame(self)
        self.configContainer.pack(fill="both",ipadx=20)
        
        self.label2 = Tkinter.Label(self.configContainer)
        self.label2.pack(pady=12, padx=5,side="left")
        self.label2["text"] = "Search at:"
        
        self.search_at  = ["FilesTube","Google"]
        self.search     = Tkinter.StringVar()
        self.op_search  = Tkinter.OptionMenu(self.configContainer, 
                                             self.search,
                                             *self.search_at)
        self.search.set("FilesTube")
        self.op_search.pack(side="left",pady=5, padx=5)
        
        self.count_sb = Tkinter.Spinbox(self.configContainer)
        self.count_sb["from"]   = 0
        self.count_sb["to"]     = 100
        self.count_sb.pack(pady=5,padx=5,side="right")
        
        self.label3 = Tkinter.Label(self.configContainer)
        self.label3.pack(pady=12, padx=2,side="right")
        self.label3["text"] = "Results:"
        
        self.configContainer2=Tkinter.Frame(self)
        self.configContainer2.pack(fill="both",ipadx=20)
        
        self.label4 = Tkinter.Label(self.configContainer2)
        self.label4.pack(pady=12, padx=5,side="left")
        self.label4["text"] = "Search for filetype:"
        
        self.filetype_lst   = ["all","rar","mp3","mp4","zip","mpeg","mpg"]
        self.filetype       = Tkinter.StringVar()
        self.filetype_op    = Tkinter.OptionMenu(self.configContainer2, 
                                             self.filetype,
                                             *self.filetype_lst)
        self.searchEntry = Tkinter.Entry(self)
        self.searchEntryVar = Tkinter.StringVar()
        self.searchEntryVar.set("Enter search keywords...")
        self.searchEntry["textvariable"] = self.searchEntryVar
        self.searchEntry.pack(pady=5, padx=5, fill="x")
        
        self.label5 = Tkinter.Label(self.configContainer2)
        self.label5.pack(pady=12, padx=5,side="right")
        
        self.buttonContainer=Tkinter.Frame(self)
        self.buttonContainer.pack(fill="both")
        
        self.searchButton = Tkinter.Button(self.buttonContainer)
        self.searchButton.pack(side="right",padx=5,pady=5,ipadx=10)
        self.searchButton["text"] = "Search"
        self.searchButton["command"] = self.__startSearch
        
        self.cancelButton = Tkinter.Button(self.buttonContainer)
        self.cancelButton.pack(side="right",padx=5,pady=5)
        self.cancelButton["text"] = "Cancel"
        self.cancelButton["command"] = self.__cancelSearch
    
        self.filetype.set("all")
        self.filetype_op.pack(side="left",pady=5, padx=5)
        
        self.link_box = Tkinter.Listbox(self)
        self.link_box.pack(pady=5, padx=5,side="top",fill="both")
        
        self.openButton = Tkinter.Button(self)
        self.openButton.pack(side="left",padx=5,pady=5,ipadx=50)
        self.openButton["text"] = "Open"
        self.openButton["command"] = self.__open_in_browser
        
        self.linkButton = Tkinter.Button(self)
        self.linkButton.pack(side="right",padx=5,pady=5,ipadx=50)
        self.linkButton["text"] = "Show Rapidshare links"
        self.linkButton["command"] = self.__show_links
        
    def __cancelSearch(self):
        
        self.check=False
        self.label5["text"] = ""
        
        
    def __startSearch(self):
        
        if self.searchEntryVar.get() == "Enter search keywords...":
            return
        self.label5["text"] = "Searching..."
        self.rs_search = Search()
        self.rs_search.start()

        #if tkMessageBox.showinfo("Searching", "Raprac is Searching"):
            
    def __fillMenuBar(self):
        self.menuFile = Tkinter.Menu(self.menuBar, tearoff=False)
        self.menuFile.add_command(label="End", command=exit)
        
        self.menuBar.add_cascade(label="File", menu=self.menuFile)
        
        self.menuHelp = Tkinter.Menu(self.menuBar, tearoff=False)
        self.menuHelp.add_command(label="Info...", command=self.open_info_window)
        
        self.menuBar.add_cascade(label="Help", menu=self.menuHelp)
        
    def searchFilesTube(self):
        self.check=True
        checked_links = []
        self.finder = FilesTubeSearch(self.searchEntryVar.get().split(),
                                      ["rapidshare"],
                                      [self.filetype.get()])
        for nr in range(2,20):
            for link in self.finder.get_link_list():
                if not self.check:
                    return
                
                if link in checked_links:
                    continue
                checked_links.append(link)
                if not "filestube" in link:
                    continue
                if self.link_box.size() == int(self.count_sb.get()):
                    return
                try:
                    if Finder(link).get_rs_link_list():
                        self.link_box.insert("end", link)
                except:
                    continue

            self.finder.set_page_nr(nr)
            self.finder.reload_page()
            
        self.label5["text"] = ""
            
    def searchGoogle(self):
        checked_links = []
        self.finder = GoogleSearch(keyword_list=self.searchEntryVar.get().split(),
                                   host_list=["rapidshare"],
                                   filetype_list=[self.filetype.get()])
        for nr in range(1,100):
            for link in self.finder.get_link_list():
                 if link in checked_links:
                     continue
                 checked_links.append(link)
                 if "google" in link:
                     continue
                 if self.link_box.size() == int(self.count_sb.get()):
                     return
                 try:
                     if Finder(link).get_rs_link_list():
                         self.link_box.insert("end", link)
                 except:
                     continue
            print nr
            self.finder.set_page_nr(nr)
            self.finder.reload_page()
            
        self.label5["text"] = ""
    
    def __open_in_browser(self):
        index = self.link_box.curselection()
        if index:
            webbrowser.open(self.link_box.get(index))
    
    def __show_links(self):
        if not self.link_box.curselection():
            return
        link = self.link_box.get(self.link_box.curselection())
        link_list = Finder(link).get_rs_link_list()
        conf = Tkinter.Tk()
        conf.title("Links")
        conf.resizable(width=False,height=False)
        self.link_window = ShowLinks(rs_link_list=link_list,master=conf)
        self.link_window.mainloop()
    
    def open_info_window(self):
        conf = Tkinter.Tk()
        conf.title("Info")
        conf.resizable(width=False,height=False)
        self.info_window = Info(master=conf)
        self.info_window.mainloop()
        
    def do_nothing(self):
        print "[*] Nothing"

        
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.title("raprac")
    root.resizable(width=False,height=False)
    app = Raprac(master=root)
    app.mainloop()
        
