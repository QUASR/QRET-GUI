#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   Meter class
#       displays a meter that can fill or empty

from config import *

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

    def reset(self):
        self.value = 0
        self.draw()

    def destroy(self):
        self.canvas.destroy()
