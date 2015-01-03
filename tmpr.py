#!/usr/bin/python
import math as m
import Tkinter as tk
import ttk
from Meter import *
import requests
from metar import Metar

class Appl(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.value=tk.StringVar()
        self.value.set(0)
        self.locations=["KBIL","KBOS","KBZN","KMSP","KGPZ"]
        self.location=tk.StringVar()
        self.location.trace("w",self.setloc)
        print self.locations
        self.createwidgets()
        self.location.set(self.locations[0])
        #self.after(1*60*1000,func=self.getval)

    def createwidgets(self):
        top=self.winfo_toplevel()
        top.resizable(0,0)
        #top.rowconfigure(0,weight=1)
        #top.columnconfigure(0,weight=1)
        #self.rowconfigure(1,weight=1)
        #self.columnconfigure(0,weight=1)
        #self.label=tk.Label(self,textvariable=self.value,width=5,
        #                    height=1,
        #                    font=("Helvetica",-20,""),relief="raised")
        #self.label.grid(row=0,column=1,sticky=tk.E)
        self.quitButton=tk.Button(self,text="Quit",
                                  command=self.quit,relief="raised")
        self.quitButton.grid(row=0,column=0)
        #self.scale=tk.Scale(self,bg="#dfc0c0",activebackground="#800000",
        #                    variable=self.value, length=225,relief="raised",
        #                    resolution=0.3,from_=-5.1,to=101.1,
        #                    command=self.cmd)
        #self.scale.grid(row=1,column=0,sticky=tk.N+tk.S)
        self.e=ttk.Combobox(self,values=self.locations,state='readonly',
                            textvariable=self.location)
        #self.e.state('readonly')
        self.e.grid(row=0,column=1,sticky=tk.E)
        self.m=Meter(self,width=550,height=500,from_=-40,to=120,)
        self.m.grid(row=1,column=1)
        #self.getval()

    def setloc(self,*args):
        print "setloc here", args
        self.location.set(self.location.get().upper())
        if hasattr(self, "callback"): self.after_cancel(self.callback)
        self.getval()

    def stats(self):
        print "height",self.m.config("height")[4]
        print "width", self.m.config("width")[4]
        self.m.stats()

    def cmd(self,x):
        pass
        #self.m.set(x)

    def getval(self):
        print "Callback here."
        params={'station_ids': self.location.get(), 'chk_metars': 'true', 'std_trans':'standard'}
        r=requests.get("http://www.aviationweather.gov/adds/metars", params=params)
        w=r.text
        ws=w.index(self.location.get())
        w=w[ws:]
        we=w.index("<")
        w=w[:we]
        #print w
        self.st=Metar.Metar(w)
        #print self.st.string()
        self.m.set(self.st.temp.value()*9./5.+32.0)
        self.callback=self.after(10*60*1000,func=self.getval)


app=Appl()
app.master.title('Meter Widget')
app.mainloop()
