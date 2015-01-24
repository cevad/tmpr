#!/usr/bin/python
import math as m
import Tkinter as tk
from sys import float_info as sfi
import sys

class Meter(tk.Canvas):
    """ DOC STRING """
    def __init__(self,master, from_=0, to=100,
                 tickminor=1,tickmajor=5,
                 **kwargs):
        tk.Canvas.__init__(self,master,highlightthickness=0,**kwargs)
        self.r=0.9
        self.dotsize=15
        self.ring=0.8
        self._x=0
        self._high=-sfi.min
        self._low=sfi.max
        self._tickminor=tickminor
        self._tickmajor=tickmajor
        self.from_=float(from_)
        self.to=float(to)
        self.setsizes(int(self.config("width")[4]),int(self.config("height")[4]))
        self._ids={}
        # High/Low wedges
        self._ids['high']=self.create_arc(self.cx-self.ringsize/2,
                                   self.cy-self.ringsize/2,
                                   self.cx+self.ringsize/2,
                                   self.cy+self.ringsize/2,
                                   style=tk.PIESLICE,fill="#fdd",
                                   width=0,
                                   start=-45, extent=135)
        self._ids['low']=self.create_arc(self.cx-self.ringsize/2,
                                  self.cy-self.ringsize/2,
                                  self.cx+self.ringsize/2,
                                  self.cy+self.ringsize/2,
                                  style=tk.PIESLICE,fill="#ccf",
                                  width=0,
                                  start=90, extent=135)
        # The dot in the center
        self._ids['oval']=self.create_oval(self.cx-self.dotsize/2,self.cy-self.dotsize/2,
                         self.cx+self.dotsize/2,self.cy+self.dotsize/2,
                         fill="#000")
        # The Arc of the meter
        self._ids['arc']=self.create_arc(self.cx-self.ringsize/2,
                                         self.cy-self.ringsize/2,
                                         self.cx+self.ringsize/2,
                                         self.cy+self.ringsize/2,
                                         style=tk.ARC,
                                         start=-45, extent=270,
                                         width=3)
        # The meter pointer
        self._ptr=self.create_line(self.cx,self.cy,
                                  0,0,
                                  width=2,arrow=tk.LAST,arrowshape=(24,30,10))
        # The text value.
        tsize=min(self.cx,self.cy)/5
        self._txt=self.create_text(0,0,text="",
                                  font=("helvetica",-tsize,"italic"))
        # Minor ticks
        self._minorticks=[]
        for i in range(int((self.to-self.from_)/self._tickminor)):
            th=i*self._tickminor+self.from_ 
            theta=(3./4.+(th-self.from_)/(self.to-self.from_)*3./2.)*m.pi
            ix=self.ringsize/2.0*m.cos(theta)+self.cx
            iy=self.ringsize/2.0*m.sin(theta)++self.cy
            ox=self.ringsize/1.95*m.cos(theta)+self.cx
            oy=self.ringsize/1.95*m.sin(theta)++self.cy
            self._minorticks.append(self.create_line(ix,iy,ox,oy,width=1,))
        # Major ticks and Labels
        self._majorticks=[]
        self._majorlabels=[]
        for i in range(int((self.to-self.from_)/self._tickmajor)):
            th=i*self._tickmajor+self.from_ 
            theta=(3./4.+(th-self.from_)/(self.to-self.from_)*3./2.)*m.pi
            ix=self.ringsize/2.0*m.cos(theta)+self.cx
            iy=self.ringsize/2.0*m.sin(theta)++self.cy
            ox=self.ringsize/1.90*m.cos(theta)+self.cx
            oy=self.ringsize/1.90*m.sin(theta)++self.cy
            tx=self.ringsize/1.75*m.cos(theta)+self.cx
            ty=self.ringsize/1.75*m.sin(theta)++self.cy

            self._majorticks.append(self.create_line(ix,iy,ox,oy,width=2))
            self._majorlabels.append(
                self.create_text(tx,ty,
                                 text="%4.0f"%th,
                                 font=("helvetica",-int(self.ringsize/30),"bold"))
            )
        self.bind('<Configure>',self.resize)

    def set(self,x):
        x=float(x)
        self._x=x
        theta=(3./4.+(x-self.from_)/(self.to-self.from_)*3./2.)*m.pi
        px=self.ringsize/2.0*m.cos(theta)+self.cx
        py=self.ringsize/2.0*m.sin(theta)++self.cy
        self.coords(self._ptr,self.cx,self.cy,px,py)
        self.itemconfigure(self._txt, text="%4.0f"%x)
        if self._x>self._high: self._high=self._x
        if self._x<self._low: self._low=self._x
        thetaH=(3./4.+(self._high-self.from_)/(self.to-self.from_)*3./2.)*m.pi
        thetaL=(3./4.+(self._low-self.from_)/(self.to-self.from_)*3./2.)*m.pi
        self.itemconfigure(self._ids['high'],
                           start=-theta/m.pi*180,
                           extent=-(thetaH-theta)/m.pi*180)
        self.itemconfigure(self._ids['low'],
                           start=-theta/m.pi*180,
                           extent=-(thetaL-theta)/m.pi*180)
    def reset(self):
        self._high=self._x
        self._low=self._x
        self.set(self._x)

    def resethigh(self):
        self._high=self._x
        self.set(self._x)

    def resetlow(self):
        self._low=self._x
        self.set(self._x)

    def stats(self):
        print self.coords(self._ptr)
        print  self.r

    def setsizes(self,width,height):
        h=min(height,self.r*width)
        w=min(width,height/self.r)
        hm=(height-h)/2
        wm=(width-w)/2
        self.cx=int(width/2)
        self.cy=int(height/2+w*(1-self.r)/2)
        self.ringsize=w*self.ring
        

    def resize(self,event):
        self.configure(height=event.height,width=event.width)
        self.setsizes(event.width,event.height)
        # The Dot at the center
        self.coords(self._ids['oval'],
                    self.cx-self.dotsize/2,self.cy-self.dotsize/2,
                    self.cx+self.dotsize/2,self.cy+self.dotsize/2)
        # The meter arc
        self.coords(self._ids['arc'],
                    self.cx-self.ringsize/2,
                    self.cy-self.ringsize/2,
                    self.cx+self.ringsize/2,
                    self.cy+self.ringsize/2)
        # High Wedge
        self.coords(self._ids['high'],
                    self.cx-self.ringsize/2,
                    self.cy-self.ringsize/2,
                    self.cx+self.ringsize/2,
                    self.cy+self.ringsize/2)
        # Low Wedge
        self.coords(self._ids['low'],
                    self.cx-self.ringsize/2,
                    self.cy-self.ringsize/2,
                    self.cx+self.ringsize/2,
                    self.cy+self.ringsize/2)
        # Text Value
        self.coords(self._txt,self.cx,self.cy+int(self.ringsize/2.5))
        tsize=int(min(self.cx,self.cy)/5)
        self.itemconfigure(self._txt,
                           font=("helvetica",-tsize,"italic"))
        #the pointer
        x=self._x
        theta=(3./4.+(x-self.from_)/(self.to-self.from_)*3./2.)*m.pi
        px=self.ringsize/2.0*m.cos(theta)+self.cx
        py=self.ringsize/2.0*m.sin(theta)++self.cy
        self.coords(self._ptr,self.cx,self.cy,px,py)

        # Minor ticks
        for i in range(len(self._minorticks)):
            th=i*self._tickminor+self.from_ 
            theta=(3./4.+(th-self.from_)/(self.to-self.from_)*3./2.)*m.pi
            ix=self.ringsize/2.0*m.cos(theta)+self.cx
            iy=self.ringsize/2.0*m.sin(theta)++self.cy
            ox=self.ringsize/1.95*m.cos(theta)+self.cx
            oy=self.ringsize/1.95*m.sin(theta)++self.cy
            self.coords(self._minorticks[i],ix,iy,ox,oy)
        # Major ticks and labels
        for i in range(len(self._majorticks)):
            th=i*self._tickmajor+self.from_ 
            theta=(3./4.+(th-self.from_)/(self.to-self.from_)*3./2.)*m.pi
            ix=self.ringsize/2.0*m.cos(theta)+self.cx
            iy=self.ringsize/2.0*m.sin(theta)++self.cy
            ox=self.ringsize/1.90*m.cos(theta)+self.cx
            oy=self.ringsize/1.90*m.sin(theta)++self.cy
            tx=self.ringsize/1.75*m.cos(theta)+self.cx
            ty=self.ringsize/1.75*m.sin(theta)++self.cy
            self.coords(self._majorticks[i],ix,iy,ox,oy)
            self.coords(self._majorlabels[i],tx,ty)
            self.itemconfigure(self._majorlabels[i],
                               font=("helvetica",-int(self.ringsize/30),"bold"))

