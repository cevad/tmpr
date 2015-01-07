#!/usr/bin/python
import math as m
import Tkinter as tk
import ttk
from Meter import *
import requests
from metar import Metar
import datetime

class Appl(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.value=tk.StringVar()
        self.value.set(0)
        self.locations=["KBIL","KBOS","KBZN","KMSP","KGPZ"]
        self.location=tk.StringVar()
        self.location.trace("w",self.setloc)
        self.createwidgets()
        self.location.set(self.locations[0])


    def createwidgets(self):
        # Make top window resizeable.
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        # Quit Button
        self.quitButton=tk.Button(self,text="Quit",
                                  command=self.quit,relief="raised")
        self.quitButton.grid(row=0,column=0,sticky=tk.W)
        #self.scale=tk.Scale(self,bg="#dfc0c0",activebackground="#800000",
        #                    variable=self.value, length=225,relief="raised",
        #                    resolution=0.3,from_=-5.1,to=101.1,
        #                    command=self.cmd)
        #self.scale.grid(row=1,column=0,sticky=tk.N+tk.S)
        self.e=ttk.Combobox(self,values=self.locations,state='readonly',
                            textvariable=self.location)
        self.e.grid(row=0,column=1,sticky=tk.E)
        self.m=Meter(self,width=300,height=300,from_=-40,to=120)
        self.m.grid(row=1,column=0,columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S)
        # time data
        self.uptime=tk.StringVar()
        self._tleft=ttk.Label(self,anchor=tk.CENTER,textvariable=self.uptime)
        self._tleft.grid(row=1,column=0,sticky=tk.W+tk.S)
        self.downtime=tk.StringVar()
        self._tright=tk.Label(self,textvariable=self.downtime)
        self._tright.grid(row=1,column=1,sticky=tk.E+tk.S)
        # site label
        self._sitename=tk.StringVar()
        self.site=ttk.Label(self, textvariable=self._sitename,
                                 font=("Comic Sans", -24,''))
        self.site.grid(row=1,column=0,columnspan=2,sticky=tk.S)
        # bindings
        


    def setloc(self,*args):
        #print "setloc here", args
        self.location.set(self.location.get().upper())
        if hasattr(self, "callback"): self.after_cancel(self.callback)
        self.getval()

    def stats(self):
        print "height",self.m.config("height")[4]
        print "width", self.m.config("width")[4]
        self.m.stats()

    def cmd(self,x):
        pass

    def getval(self):
        #print "Callback here."
        params={'station_ids': self.location.get(), 'chk_metars': 'true', 'std_trans':'standard'}
        try:
            r=requests.get("http://www.aviationweather.gov/adds/metars", params=params)
            w=r.text
            ws=w.index(self.location.get())
            w=w[ws:]
            we=w.index("<")
            w=w[:we]
            self.st=Metar.Metar(w)
            self._sitename.set(params['station_ids'])
        except:
            # Just use old values if connection problems
            pass
        self.m.set(self.st.temp.value()*9./5.+32.0)
        # update Labels in corners
        self.uptime.set(str(self.st.time))
        self.downtime.set(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
        # Set up next check
        self.callback=self.after(10*60*1000,func=self.getval)


app=Appl()
app.master.title('Meter Widget')
app.mainloop()
