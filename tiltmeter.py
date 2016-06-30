#   QRET Rocket GUI

#   Eric Donders
#   May 18, 2016

#   Tiltmeter Class
#       displays rocket tilt angle

from config import *

class Tiltmeter():
    def __init__(self, parent, display=True):
        self.canvas = Canvas(parent, background='white', highlightthickness=0)
        self.parent = parent
        self.display = display

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self.tilt = None

    def place(self, x, y, width, height):
        if self.display:
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.canvas.place(x=x, y=y, width=width, height=height)
            self.draw()

    def draw(self):
        self.canvas.delete(tkinter.ALL)
        self.canvas.create_oval((0, 0, self.width-1, self.height-1))
        self.canvas.create_line((self.width/2, self.height/2, self.width/2, 0), fill="black", width=2)
        if self.tilt is not None:
            text = str(self.tilt)+u"\u00b0"
            d = min(self.width, self.height)
            self.canvas.create_arc((d/4,d/4,3*d/4,3*d/4), start=90, extent=-self.tilt, style=tkinter.ARC)
            self.canvas.create_line((self.width/2-d/2*sin(radians(self.tilt)), self.height/2+d/2*cos(radians(self.tilt)), self.width/2+d/2*sin(radians(self.tilt)), self.height/2-d/2*cos(radians(self.tilt))), fill="red", width=2)
        else:
            text = "-"+u"\u00b0"
        self.canvas.create_text((0, 0), anchor=tkinter.NW, font=getfont(), text=text)

    def send(self, tilt):
        self.tilt = tilt
        self.refresh()

    def show(self, show=True):
        self.display = show
        if show:
            self.canvas.lift(self.parent)
        else:
            self.canvas.lower(self.parent)

    def refresh(self):
        self.place(self.x, self.y, self.width, self.height)

    def reset(self):
        self.tilt = None
        self.draw()
        
    def destroy(self):
        self.canvas.get_tk_widget().destroy()
