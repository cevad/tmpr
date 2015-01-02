#!
import math as m
import Tkinter as tk

class Meter(tk.Canvas):
    """ DOC STRING """
    def __init__(self,master, from_=0, to=100,
                 tickminor=1,tickmajor=5,
                 **kwargs):
        tk.Canvas.__init__(self,master,**kwargs)
        self.from_=float(from_)
        self.to=float(to)
        self.cx=int(self.config("width")[4])/2
        self.cy=int(self.config("height")[4])/2
        dotsize=15
        self.ringsize=min(self.cx, self.cy)*1.7
        self.create_oval(self.cx-dotsize/2,self.cy-dotsize/2,
                         self.cx+dotsize/2,self.cy+dotsize/2,
                         fill="#000")
        self.create_arc(self.cx-self.ringsize/2,self.cy-self.ringsize/2,
                         self.cx+self.ringsize/2,self.cy+self.ringsize/2,
                        style=tk.ARC,
                        start=-45, extent=270,
                        width=3)
        self.ptr=self.create_line(self.cx,self.cy,
                                  0,0,
                                  width=2,arrow=tk.LAST,arrowshape=(24,30,10))
        self.r=range(int((self.to-self.from_)/tickminor))
        self.r=[i*tickminor+self.from_ for i in self.r]
        for th in self.r:
            theta=(3./4.+(th-self.from_)/(self.to-self.from_)*3./2.)*m.pi
            ix=self.ringsize/2.0*m.cos(theta)+self.cx
            iy=self.ringsize/2.0*m.sin(theta)++self.cy
            ox=self.ringsize/1.95*m.cos(theta)+self.cx
            oy=self.ringsize/1.95*m.sin(theta)++self.cy
            self.create_line(ix,iy,ox,oy,width=1,)
        self.r=range(int((self.to-self.from_)/tickmajor))
        self.r=[i*tickmajor+self.from_ for i in self.r]
        for th in self.r:
            theta=(3./4.+(th-self.from_)/(self.to-self.from_)*3./2.)*m.pi
            ix=self.ringsize/2.0*m.cos(theta)+self.cx
            iy=self.ringsize/2.0*m.sin(theta)++self.cy
            ox=self.ringsize/1.90*m.cos(theta)+self.cx
            oy=self.ringsize/1.90*m.sin(theta)++self.cy
            tx=self.ringsize/1.79*m.cos(theta)+self.cx
            ty=self.ringsize/1.79*m.sin(theta)++self.cy
            self.create_line(ix,iy,ox,oy,width=2,)
            self.create_text(tx,ty,text="%4.1f"%th)
        self.txt=self.create_text(self.cx,self.cy*1.8,text="",
                                  font=("times",-75,"italic"))

    def set(self,x):
        x=float(x)
        theta=(3./4.+(x-self.from_)/(self.to-self.from_)*3./2.)*m.pi
        px=self.ringsize/2.0*m.cos(theta)+self.cx
        py=self.ringsize/2.0*m.sin(theta)++self.cy
        self.coords(self.ptr,self.cx,self.cy,px,py)
        self.itemconfigure(self.txt, text="%4.1f"%x)

    def stats(self):
        print self.coords(self.ptr)
        print  self.r
