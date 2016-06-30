#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   Configuration constants

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style, rcParams

from tkinter import Frame, Tk, Menu, PhotoImage, Canvas, Button, Scrollbar, Listbox, Text, ttk, filedialog
from math import *
import time, serial, tkinter
from serial.serialutil import SerialException

matplotlib.use("TkAgg")
rcParams.update({'figure.autolayout': True})
style.use("ggplot")

global bw, stage, resolution
bw = 10 # spacing between widgets
stage = 'a' # rocket stage
resolution = '1366x768' # wxh

def getfont(size=14):
    return ('Helvetica', size)
