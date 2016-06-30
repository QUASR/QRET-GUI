# QUASR Rocket GUI

#   Eric Donders
#   December 15, 2014

# Import modules
from tkinter import *
from math import *
import time, serial, tkinter
from serial.serialutil import SerialException

# Global variables
global bw, serialport, stage, logfile
bw = 10 # spacing between widgets
serialport = 3 #COM4
logfile = "Q_log.txt" # log file
stage = 'a' # rocket stage


# Mainwindow class: main window that houses all widgets
class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()
        self.widgets = ()
        
    def initUI(self):
        self.parent.geometry('1000x800')
        self.parent.title("QUASR Rocket GUI")
        self.pack(fill=BOTH, expand=1)

    def setwidgets(self, widgets):
        self.widgets = widgets
        
    def fit_widgets(self):
        def _r(e):
            rw = self.winfo_width()
            rh = self.winfo_height()
            self.widgets[0].place(x=300+bw, y=bw, height=rh-2*bw, width=rw-300-3*bw)
            self.widgets[1].place(x=bw, y=rh/2+bw/2, height=rh/2-1.5*bw, width=300-bw)
            self.widgets[2].place(x=bw, y=bw, height=rh/2-1.5*bw, width=300-bw)
        return _r

    def destroy(self):
        for widget in self.widgets:
            widget.destroy()



# Plot class: used for displaying data on a graph
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

    def send(self, xpt, ypt):
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



# Map class
class Map():

    def __init__(self, parent, imagefile, tlc_coords, brc_coords, width, height, zoom = 1):
        self.parent = parent
        self.image = PhotoImage(file = imagefile)
        self.tlc_coords = tlc_coords
        self.brc_coords = brc_coords
        self.ns_span = self.tlc_coords[0] - self.brc_coords[0]
        self.ew_span = self.tlc_coords[1] - self.brc_coords[1]
        self.width = width
        self.height = height
        self.zoom = zoom



# Meter class
class Meter():

    def __init__(self, parent, maximum, minimum):
        self.parent = parent
        self.maximum = maximum
        self.minimum = minimum
        self.value = 0
        self.canvas = Canvas(parent, background='white')
        self.color = 'white'

    def place(self, x, y, width, height):
        # fit to current window size
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.x = x # x position
        self.y = y # y position
        self.width = width # width of widget
        self.height = height # height of widget
        # draw plot
        self.draw()

    def draw(self):
        # clear canvas
        self.canvas.create_rectangle(0,0,self.width*self.value/self.maximum,self.height, fill=self.color, width=0)

    def send(self, value):
        if value <= self.maximum:
            if value > self.minimum:
                self.value = value
            else:
                self.value = self.minimum
        else:
            self.value = self.maximum
        if self.value >= self.maximum*0.6:
            self.color = 'green'
        elif self.value >= self.maximum*0.4:
            self.color = 'yellow'
        elif self.value >= self.maximum*0.2:
            self.color = 'orange'
        else:
            self.color = 'red'
        self.draw()



# MapGraph class
class MapGraph():

    def __init__(self, parent, maps, zoom=1):
        self.parent = parent
        self.maps = maps
        self.map = maps
        self.zoom = zoom
        self.canvas = Canvas(parent, background='white', highlightthickness=0)

        self.latdata = [0]
        self.longdata = [0]

    def place(self, x, y, width, height):
        # fit to current window size
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.x = x # x position
        self.y = y # y position
        self.width = width # width of widget
        self.height = height # height of widget
        # draw plot
        self.draw()

    def draw(self):
        # clear canvas
        self.canvas.delete(ALL)
        if self.map != 0:
            self.canvas.create_image((self.width/2, self.height/2), image=self.map.image)
            px0 = 0
            py0 = 0
            for i in range(0,len(self.latdata)):
                px = self.width/2-self.map.width/2 - (self.longdata[i]-self.map.tlc_coords[1]) * self.map.width/self.map.ew_span
                py = self.height/2-self.map.height/2 - (self.latdata[i]-self.map.tlc_coords[0]) * self.map.height/self.map.ns_span
                self.canvas.create_oval(px-2,py-2,px+2,py+2,fill="red")
                if px0 != 0 and px0 < 3000:
                    self.canvas.create_line((px,py,px0,py0),fill="red")
                px0 = px
                py0 = py
                

    def send(self, latpt, longpt):
        self.latdata.append(latpt)
        self.longdata.append(longpt)

        self.draw()

    def destroy(self):
        self.canvas.destroy()
        




# Serialmonitor class
class SerialMonitor():

    def __init__(self, parent, hplot, mplot, meter):
        global serialport, logfile
        self.scrollbar = Scrollbar(parent)
        spintxt = StringVar()
        spintxt.set(str(serialport+1))
        self.spinbox = Spinbox(parent, from_=0, to=4 ,command=self.changeport, state='readonly', textvariable=spintxt, font=getfont(12))
        self.spinlabel = Label(parent, text="COM port:", bg="white", font=getfont(12))
        self.listbox = Listbox(parent, bg='white', yscrollcommand=self.scrollbar.set, font=getfont(10))
        self.scrollbar.config(command=self.listbox.yview)
        self.parent = parent
        self.hplot = hplot
        self.mplot = mplot

        self.meter = meter
        
        self.t0 = 0 # replace later
        str_ = "Started "+str(time.asctime(time.localtime(time.time())))
        self.listbox.insert(END, str_)
        self.file = open(logfile, 'a')
        self.file.write(str_+"\n\r")

        self.serial = serial.Serial(baudrate=9600, timeout = 0.05)
        self.serial.port = serialport
        self.log("Trying to connect to COM"+str(serialport+1)+"...")
        self.serialopen = False
        self.authenticated = False
        
    def place(self, x, y, width, height):
        self.scrollbar.place(x=x+width-16, y=y, width=16, height=height-20-bw)
        self.spinbox.place(x=x+70+bw, y=y+height-20, width=30, height=20)
        self.listbox.place(x=x, y=y, width=width-16, height=height-20-bw)
        self.spinlabel.place(x=x, y=y+height-20, width=70, height=20)
        self.meter.place(x=x+130, y=y+height-20, width=width-130, height=20)
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        
    def receive(self):
        if not self.serialopen:
            try:
                self.serial.open()
                self.serialopen = True
                self.message("Connected to device on COM"+str(serialport+1))
            except Exception:
                pass
        
        elif not self.authenticated:
            if self.serial.inWaiting() > 0:
                self.authenticated = True
                self.message("Authenticated")
        
        else:
            first = self.serial.read().decode()
            if first != "$":
                self.file.write(first)
            else:
                try:
                    msg = self.serial.read(68).decode()
                    self.file.write("$" + str(msg))
                    ID = msg[6:12]
                    flag = msg[14]
                    fixtime = msg[15:21]
                    HDOP = msg[48:52]
                    VDOP = msg[60:64]
                    V = 5.0 / 1023 * int(msg[65:68],16)
                    self.meter.send(V)
                    latitude = float(msg[22:24]) + float(msg[24:31])/60
                    longitude = float(msg[33:36]) + float(msg[36:43])/60
                    nsatellites = int(msg[45:47])
                    altitude = float(msg[53:59])
                    tval = time.clock()-self.t0
                    self.hplot.send(tval, altitude)
                    self.mplot.send(latitude,longitude)
                    if self.t0 == 0:
                        self.t0 = time.clock()
                except:
                    pass

        # Repeat every sec
        self.parent.after(90, self.receive)

    def command(self, cmd):
        if self.serialopen and self.authenticated:
            self.serial.write(cmd)
        
    def changeport(self):
        global serialport
        newport = int(self.spinbox.get())-1
        if newport != serialport:
            self.message("Serial port changed to COM"+str(newport+1))
            serialport = newport
            self.serial.close()
            self.serial.port = newport
            self.serialopen = False

    def message(self, msg):
        t = time.localtime(time.time())
        self.listbox.insert(END, str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)+" > "+msg)
        self.log(msg)

    def log(self, msg):
        t = time.localtime(time.time())
        str_ = str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)+" > "+msg
        print(str_)
        self.file.write(str_+"\n\r")

    def setcommandcenter(self, commandcenter):
        self.commandcenter = commandcenter
            
    def destroy(self):
        self.scrollbar.destroy()
        self.listbox.destroy()
        if self.serialopen:
            self.serial.close()
            self.log("Closed serial device connection")
        self.file.write("\n\r")
        self.file.close()
        print("Closed log file")
        
                            
def main():
    root = Tk()
    root.minsize(800,600)
    app = MainWindow(root)

    k_map = Map(app, "Maps\Kingston_z1.gif", (44.2296,76.4928), (44.2224,76.4856), 626, 872)
    u_map = Map(app, "Maps\Green_River_z2.gif", (38.850,110.25), (38.830,110.21), 1250, 810)
    mapplot = MapGraph(app,(k_map))
    altplot = Plot(app, ylabel="Altitude (m)", altplot=True)
    battery_meter = Meter(app, 4.3, 3)
    datamonitor = SerialMonitor(app, altplot, mapplot, battery_meter)
    widgets = (mapplot, altplot, datamonitor)
    app.setwidgets(widgets)
    
    datamonitor.receive()
    app.bind("<Configure>", app.fit_widgets())
    app.mainloop()
    

def getfont(size=14):
    return ('Helvetica', size)

if __name__ == '__main__':
    main()
    
