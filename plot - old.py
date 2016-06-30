#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   Plot Class
#       displays data on a graph

from config import *

class Plot():
    def __init__(self, parent, xmax=10, ymax=100, ymin=0, numy=1, xlabel="Time (s)", ylabel="DEFAULT", colours=['red','blue','green'], altplot=False):
        # create canvas for drawing on
        self.canvas = Canvas(parent, background='white', highlightthickness=0)
        self.parent = parent
        # lists for data, and min and max values for the plot
        self.xdata=[0]
        self.ydata=[] # 2D array, one sub-array per data set
        if numy > 3:
            raise Exception("Can't currently have more than three data series per plot")
        for i in range(0,numy):
            self.ydata.append([0])
        self.xmax=xmax
        self.xstep=xmax
        self.ymax=ymax
        self.ymin=ymin
        self.ystep=ymax
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.colours=colours
        self.lsz=25
        self.altplot=altplot
        
    def place(self, x, y, width, height):
        # fit to current window size
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.x = x # x position
        self.y = y # y position
        self.width = width # width of widget
        self.height = height # height of widget
        self.plotheight = height-2*bw-2*self.lsz # height of plot area
        self.plotwidth = width-2*bw-2*self.lsz # width of plot area
        self.zeroy = bw+self.lsz+self.plotheight*self.ymax/(self.ymax-self.ymin) # location of y=0
        # draw plot
        self.draw()
        
    def draw(self):
        # clear canvas
        self.canvas.delete(ALL)
        d = bw+self.lsz # space for title and x labels
        dw = bw+2*self.lsz # horizontal space for wide y labels
        # draw plot lines
        if len(self.xdata) > 1:
            for j in range(0,len(self.ydata)):
                coords = []
                for i in range(0,len(self.xdata)):
                    coords.append(self.xdata[i]/self.xmax*(self.plotwidth) + 75)
                    coords.append(-self.ydata[j][i]/self.ymax*(self.plotheight) + self.zeroy)
                self.canvas.create_line(coords, fill=self.colours[j])
        if self.altplot and self.ymax > 3048: # draw line at 10,000ft
            print("Test")
            goaly = -3048/self.ymax*(self.plotheight) + self.zeroy
            self.canvas.create_line(dw, goaly, dw+self.plotwidth, goaly, fill='#000ddd000')
        # draw axes
        self.canvas.create_rectangle(dw, d, dw+self.plotwidth, d+self.plotheight, outline="#aaaaaaaaa")
        self.canvas.create_line(dw, d, dw, d+self.plotheight, width=2)
        self.canvas.create_line(dw, self.zeroy, dw+self.plotwidth, self.zeroy, width=1.5)
        # draw title
        self.canvas.create_text(dw+self.plotwidth/2, bw, text=self.ylabel+" vs "+self.xlabel, anchor=tkinter.N, font=getfont(14))
        # draw y axis labels
        labelstep = floor(self.ymax/5)
        val = 5*labelstep # start with maximum value
        while val >= self.ymin:
            ypos=d+(self.zeroy-d)*(1-val/self.ymax) # location to draw point
            self.canvas.create_text(dw-10, ypos, text=str(val), anchor=tkinter.E, font=getfont(10))
            self.canvas.create_line(dw-5, ypos, dw, ypos)
            val -= labelstep
        # draw x axis labels
        labelstep=max(1, int(self.xmax/10))
        val = 0
        while val <= self.xmax:
            xpos = dw+self.plotwidth*val/self.xmax
            self.canvas.create_text(xpos, self.height-bw, text=str(val), anchor=tkinter.S, font=getfont(10))
            self.canvas.create_line(xpos, self.zeroy, xpos, self.zeroy+5)
            val += labelstep

    def send(self, xpt, ypt, series):
        # receive data from serial monitor
        self.xdata.append(xpt)
        while xpt > self.xmax:
            self.xmax += self.xstep
        if type(ypt) is not list and type(ypt) is not tuple:
            ypt=[ypt]
        for i in range(0,len(ypt)):
            newy = ypt[i]
            self.ydata[i].append(newy)
            while newy > self.ymax:
                self.ymax += self.ystep
            while newy < self.ymin:
                self.ymin -= self.ystep
        self.place(self.x, self.y, self.width, self.height)
        
    def destroy(self):
        self.canvas.destroy()
