#!/usr/bin/python
import math as m
import Tkinter as tk
import ttk
import xml.etree.ElementTree as ET
from Meter import *
import requests
import datetime

#evnt=0  #dbg global

class Appl(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.value=tk.StringVar()
        self.value.set(0)
        self.locations=["KBIL","KBOS","KBZN","KMSP","KGPZ"]
        self.location=tk.StringVar()
        self.createwidgets()
        self.location.set(self.locations[0])
        self.setloc()


    def createwidgets(self):
        # Make top window resizeable.
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)

        self.grip=ttk.Sizegrip(self)
        self.grip.grid(row=2,column=1,sticky=tk.SE)
        # Quit Button
        self.quitButton=tk.Button(self,text="Quit",
                                  command=self.quit,relief="raised")
        self.quitButton.grid(row=0,column=0,sticky=tk.W)
        # Reset Button
        self.resetButton=tk.Button(self,text="Reset",
                                  command=self.reset,relief="raised")
        self.resetButton.grid(row=0,column=0,sticky=tk.E)
        # To enter station id
        self.e=ttk.Combobox(self,values=self.locations,#state='readonly',
                            textvariable=self.location)
        self.e.grid(row=0,column=1,sticky=tk.E)
        # My custom widget
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
        self.e.bind("<<ComboboxSelected>>",self.setloc)
        self.e.bind("<Return>",self.keyhandler)

    def reset(self):
        self.m.reset()

    def keyhandler(self,event):
        """ Only allow 4 letter strings through to be fetched"""
        sin=self.location.get()
        if len(sin) == 4:
            self.setloc()
        else:
            self.location.set("")

    def setloc(self,*args):
        self.location.set(self.location.get().upper())
        if hasattr(self, "callback"): self.after_cancel(self.callback)
        self.getval()

    def cmd(self,x):
        pass

    def getval(self):
        try:
            wxdat=getwx(self.location.get())
            self.uptime.set(wxdat['time'])
            self.m.set(wxdat['T'])
            self._sitename.set(wxdat['sid'])
        except:
            # Just use old values if connection problems
            pass
        self.downtime.set(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        # Set up next check
        self.callback=self.after(10*60*1000,func=self.getval)
#        self.callback=self.after(1*60*1000,func=self.getval)

def getwx(sid):
    if type(sid)!=str:raise TypeError("getwx needs string argumenmt")
    sid=sid.upper()
    if len(sid)!=4:raise ValueError("getwx needs icao ident")
    params={'sid': sid, 'num': '1'}
    dsource="http://www.wrh.noaa.gov/mesowest/getobextXml.php"
    r=requests.get(dsource, params=params)
    xmlroot=ET.fromstring(r.text)
    ob=xmlroot[0]
    dat={i.get('var'):i.get('value') for i in ob}
    t=ob.get('time')
    t=str(datetime.datetime.now().year)+' '+t
    t=t[:-4]
    t1=datetime.datetime.strptime(t,"%Y %d %b %I:%M %p")
    dat['time']=str(t1)
    dat['sid']=sid
    return dat


if __name__=='__main__':
    app=Appl()
    app.master.title('Meter Widget')
    app.mainloop()
