#   QUASR Rocket GUI

#   Eric Donders
#   December 15, 2014

# Import modules
from config import *
from mainwindow import MainWindow
from plot import Plot
from airmap import Map
from meter import Meter
from mapgraph import MapGraph
from datamonitor import Datamonitor
from serialmonitor import SerialMonitor
from tabs import Tabs
#from tiltmeter import Tiltmeter
                            
def main():
    root = Tk()
    root.minsize(800,600)
    app = MainWindow(root)
    
    infotab = Tabs(app)
    k_map = Map(app, "Maps\Kingston_z1.gif", (44.2296,76.4928), (44.2224,76.4856), 626, 872)
    u_map = Map(app, "Maps\Green_River_z2.gif", (38.850,110.25), (38.830,110.21), 1250, 810)
    u_map_big = Map(app, "Maps\Green_River_Launch_Map.gif", (38.8440, 110.255), (38.8296, 110.205), 7137, 2657)
    u_map_2016 = Map(app, "Maps\GR_2016.gif", (38.82,109.99), (38.77,109.88), 1240, 666)
    
    mapplot = MapGraph(app,(u_map_2016, u_map_big, u_map, k_map), index = 0)
    dataplot = Datamonitor(app)
    altplot = Plot(app, ylabel="Altitude (m)", xinterval=float("inf"), numy=2)
    
    battery_meter = Meter(app, 4.3, 3)
    serialmonitor = SerialMonitor(app, altplot, mapplot, dataplot, battery_meter)
    infotab.add_tab(mapplot, "Map")
    infotab.add_tab(dataplot, "Plots")
    
    widgets = (infotab, altplot, serialmonitor)
    app.setwidgets(widgets)
    #serialmonitor.scan_ports()
    app.bind("<Configure>", app.fit_widgets())
    app.mainloop()


if __name__ == '__main__':
    main()
    
