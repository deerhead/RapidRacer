#!/usr/bin/env python

import Tkinter

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
        
        self.img = Tkinter.PhotoImage(file="logo.gif")
        self.cv.create_image(0,0, image=self.img, anchor="nw")
        
        self.label1 = Tkinter.Label(self)
        self.label1.pack(pady=12, padx=5)
        self.label1["text"] = "Welcome to raprac 0.1!"
        
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
        self.filetype.set("all")
        self.filetype_op.pack(side="left",pady=5, padx=5)
        
        self.searchEntry = Tkinter.Entry(self)
        self.searchEntryVar = Tkinter.StringVar()
        self.searchEntryVar.set("Enter search keywords...")
        self.searchEntry["textvariable"] = self.searchEntryVar
        self.searchEntry.pack(pady=5, padx=5, fill="x")
        
        self.buttonContainer=Tkinter.Frame(self)
        self.buttonContainer.pack(fill="both")
        
        self.search = Tkinter.Button(self.buttonContainer)
        self.search.pack(side="right",padx=5,pady=5)
        self.search["text"] = "Search"
        self.search["command"] = self.action()
    
        self.link_box = Tkinter.Listbox(self)
        self.link_box.pack(pady=5, padx=5,side="top",fill="both")
        
        self.search = Tkinter.Button(self)
        self.search.pack(side="bottom",padx=5,pady=5,ipadx=50)
        self.search["text"] = "Open"
        self.search["command"] = self.action()
        
    def __fillMenuBar(self):
        self.menuFile = Tkinter.Menu(self.menuBar, tearoff=False)
        self.menuFile.add_command(label="End", command=self.quit)
        
        self.menuBar.add_cascade(label="File", menu=self.menuFile)
        
        self.menuHelp = Tkinter.Menu(self.menuBar, tearoff=False)
        self.menuHelp.add_command(label="Info...", command=self.action)
        
        self.menuBar.add_cascade(label="Help", menu=self.menuHelp)
        
    def action(self):
        
        pass
    
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.title("raprac")
    root.resizable(width=False,height=False)
    app = Raprac(master=root)
    app.mainloop()
        