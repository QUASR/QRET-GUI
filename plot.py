#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   Plot Class
#       displays data on a graph

from config import *

class Plot():
    def __init__(self, parent, numy=1, xinterval=20, xlabel="Time (s)", ylabel="DEFAULT", colours=['red','blue','green'], display=True, xrng=0, name = "NONE"):
        # create canvas for drawing on
        self.canvas = Canvas(parent, background='white', highlightthickness=0)
        self.parent = parent
        self.numy = numy
        self.xinterval = xinterval
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.colours=colours
        self.lsz=25
        self.x=0
        self.y=0
        self.width = 100
        self.height = 100

        self.display = display
        self.xrng = xrng
        self.name = name

        # create matplotlib figure
        self.figure = Figure()
        self.plt = self.figure.add_subplot(111)
        # create canvas for displaying figure
        self.canvas = FigureCanvasTkAgg(self.figure,self.parent)
        self.reset()
        self.canvas.show()
        
    def place(self, x, y, width, height):
        if self.display:
            # fit to current window size
            self.draw()
            self.canvas.get_tk_widget().place(x=x, y=y, width=width, height=height)
            self.x = x # x position
            self.y = y # y position
            self.width = width # width of widget
            self.height = height # height of widget

    def draw(self):
        if self.display:
            self.plt.clear()
            self.plt.set_ylabel(self.ylabel)
            self.plt.set_xlabel(self.xlabel)
            for i in range(0,self.numy):
                self.plt.plot(self.xdata[i], self.ydata[i])
            self.figure.canvas.draw()


    def send(self, xpt, ypt, index):
        # receive data from serial monitor
        if index < self.numy:
            xlist = self.xdata[index]
            ylist = self.ydata[index]
            xlist.append(xpt)
            ylist.append(ypt)
            xlims = self.plt.get_xlim()
            if (xlims[1] - xlims[0]) > self.xinterval:
                new_low_lim = xlims[1] - self.xinterval
                self.plt.set_xlim(new_low_lim, xlims[1])
            while xlist[0] < self.plt.get_xlim()[0]:
                self.xdata_old[index].append(xlist.pop(0))
                self.ydata_old[index].append(ylist.pop(0))
        else:
            raise Exception("Plot index out of bounds!")

    def show(self, show=True):
        self.display = show
        if show:
            self.canvas.get_tk_widget().lift(self.parent)
        else:
            self.canvas.get_tk_widget().lower(self.parent)

    def refresh(self):
        self.place(self.x, self.y, self.width, self.height)

    def reset(self):
        # lists for data, and min and max values for the plot
        self.xdata=[]
        self.ydata=[] # 2D array, one sub-array per data set
        self.xdata_old = []
        self.ydata_old = []
        self.plt.set_xlim(0,1)
        for i in range(0,self.numy):
            self.xdata.append([0])
            self.ydata.append([0])
            self.xdata_old.append([0])
            self.ydata_old.append([0])
        
    def destroy(self):
        self.canvas.get_tk_widget().destroy()
