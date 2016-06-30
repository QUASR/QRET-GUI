#   QUASR Rocket GUI

#   Eric Donders
#   March 1, 2016

#   Datamonitor Class
#       displays data on multiple graphs

from config import *
from plot import Plot
from tiltmeter import Tiltmeter

class Datamonitor(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # create plots for drawing on
        self.accel_plot = Plot(self, ylabel="Acceleration (g)", numy=3, xrng=10, name="ACCEL")
        self.gyro_plot = Plot(self, ylabel="Angular Velocity (degrees/s)", numy=3, xrng=10, name="GYRO")
        self.mag_plot = Plot(self, ylabel="Field Strength", numy=3, xrng=10, name="MAG")
        self.plots = (self.accel_plot, self.gyro_plot, self.mag_plot)
        self.attitude_plot = Tiltmeter(self)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.plotnext = 0

    def place(self, x, y, width, height):
        # fit all plots in window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        figureheight = height/3-4/3*bw
        figurewidth = width-2*bw 
        self.accel_plot.place(x=bw, y=bw, width=figurewidth, height=figureheight)
        self.gyro_plot.place(x=bw, y=figureheight+2*bw, width=figurewidth, height=figureheight)
        self.mag_plot.place(x=bw, y=2*figureheight+3*bw, width=figurewidth-bw-figureheight, height=figureheight)
        self.attitude_plot.place(x=width-figureheight-bw, y=2*figureheight+3*bw, width=figureheight, height=figureheight) 

    def show(self):
        self.accel_plot.show(True)
        self.gyro_plot.show(True)
        self.mag_plot.show(True)
        self.attitude_plot.show(True)
        self.update()

    def hide(self):
        self.accel_plot.show(False)
        self.gyro_plot.show(False)
        self.mag_plot.show(False)
        self.attitude_plot.show(False)

    def update(self):
        self.place(self.x, self.y, self.width, self.height)

    def refresh(self):
        self.plots[self.plotnext].draw()
        self.plotnext = (self.plotnext + 1) % len(self.plots)

    def reset(self):
        for plot in self.plots:
            plot.reset()
        self.attitude_plot.reset()

    def destroy(self):
        self.accel_plot.destroy()
        self.gyro_plot.destroy()
        self.mag_plot.destroy()
