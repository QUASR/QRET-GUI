#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   MapGraph class
#       plots received GPS data on the aerial map

from config import *

class MapGraph(Frame):
    def __init__(self, parent, maps, index=0, zoom=0):
        "MapGraph constructor"
        Frame.__init__(self, parent)
        self.parent = parent
        self.maps = maps
        self.index = index
        self.map = maps[index]
        self.zoom = zoom
        self.frame = Frame()
        self.canvas = Canvas(self.frame, background='white', highlightthickness=0)
        self.zoomin_button = Button(self.frame, text="+", command=self.zoomin, width=3)
        self.zoomout_button = Button(self.frame, text="-", command=self.zoomout, width=3)
        self.canvas.bind("<ButtonPress-1>", self.startmove)
        self.canvas.bind("<ButtonRelease-1>", self.stopmove)

        self.x = 0
        self.y = 0
        self.x0 = 0
        self.y0 = 0
        self.dx = 0
        self.dy = 0
        self.width = 0
        self.height = 0

        self.reset()

    def place(self, x, y, width, height):
        # fit to current window size
        self.frame.place(x=x, y=y, width=width, height=height)
        ddx = max(0, -self.map.width/2+width/2+self.dx)
        self.dx = self.dx-ddx
        self.canvas.place(x=-self.map.width/2+width/2+self.dx-ddx, y=-self.map.height/2+height/2+self.dy, width=self.map.width, height=self.map.height)
        self.x = x # x position
        self.y = y # y position
        self.width = width # width of widget
        self.height = height # height of widget
        # draw plot
        self.draw()

    def draw(self):
        # clear canvas
        self.canvas.delete(tkinter.ALL)
        if self.map != 0:
            self.canvas.create_image((self.map.width/2, self.map.height/2), image=self.map.image)
            # plot payload coordinates
            px0 = 0
            py0 = 0
            sz = 2
            for i in range(0,len(self.pl_latdata)):
                if i == len(self.r_latdata) - 1:
                    sz = 3
                px = self.width/2-self.map.width/2 - (self.pl_longdata[i]-self.map.tlc_coords[1]) * self.map.width/self.map.ew_span
                py = self.height/2-self.map.height/2 - (self.pl_latdata[i]-self.map.tlc_coords[0]) * self.map.height/self.map.ns_span
                self.canvas.create_oval(px-sz,py-sz,px+sz,py+sz,fill="red")
                if px0 != 0 and px0 < 3000:
                    self.canvas.create_line((px,py,px0,py0),fill="red")
                px0 = px
                py0 = py
            # plot rocket coordinates
            px0 = 0
            py0 = 0
            sz = 2
            for i in range(0,len(self.r_latdata)):
                if i == len(self.r_latdata) - 1:
                    sz = 3
                px = self.width/2-self.map.width/2 - (self.r_longdata[i]-self.map.tlc_coords[1]) * self.map.width/self.map.ew_span
                py = self.height/2-self.map.height/2 - (self.r_latdata[i]-self.map.tlc_coords[0]) * self.map.height/self.map.ns_span
                self.canvas.create_oval(px-sz,py-sz,px+sz,py+sz,fill="purple")
                if px0 != 0 and px0 < 3000:
                    self.canvas.create_line((px,py,px0,py0),fill="purple")
                px0 = px
                py0 = py
            self.canvas.create_text((self.map.width/2-self.width/2-self.dx+bw, self.map.height/2+self.height/2-self.dy-bw-50), anchor=tkinter.NW, font=getfont(), text="Payload last seen at:\t"+str(self.pl_latdata[-1])+", "+str(self.pl_longdata[-1]))
            self.canvas.create_text((self.map.width/2-self.width/2-self.dx+bw, self.map.height/2+self.height/2-self.dy-bw-25), anchor=tkinter.NW, font=getfont(), text="Rocket last seen at:\t"+str(self.r_latdata[-1])+", "+str(self.r_longdata[-1]))
        self.zoomin_button.place(x = self.width-50, y = bw)
        self.zoomout_button.place(x = self.width-50, y = bw+30)

    def resize(self, direction):
        # resize air map
        self.map.resize(direction)
        self.zoom = self.map.zoom
        #self.dx = self.map.width/2-self.width/2+self.canvas.winfo_x()
        #self.dy = self.map.height/2-self.height/2+self.canvas.winfo_y()
        self.refresh()

    def zoomin(self):
        # zoom map in
        self.resize(-1)

    def zoomout(self):
        # zoom map out
        self.resize(1)

    def startmove(self, event):
        self.x0 = event.x
        self.y0 = event.y

    def stopmove(self, event):
        self.dx = self.dx+event.x-self.x0
        self.dy = self.dy + event.y - self.y0
        self.x0 = None
        self.y0 = None
        self.place(self.x, self.y, self.width, self.height)
        

    def send(self, latpt, longpt, source):
        if source == "pl":
            self.pl_latdata.append(latpt)
            self.pl_longdata.append(longpt)
        elif source == "r":
            self.r_latdata.append(latpt)
            self.r_longdata.append(longpt)

        self.draw()

    def change_map(self, index):
        if index < len(self.maps):
            self.index = index
            self.map = self.maps[index]

    def show(self):
        self.frame.lift(self.parent)

    def hide(self):
        self.frame.lower(self.parent)

    def refresh(self):
        self.place(self.x, self.y, self.width, self.height)

    def reset(self):
        self.pl_latdata = [0]
        self.pl_longdata = [0]
        self.r_latdata = [0]
        self.r_longdata = [0]
        #self.draw()

    def destroy(self):
        self.canvas.destroy()
