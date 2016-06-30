#   QUASR Rocket GUI

#   Eric Donders
#   February 18, 2016

#   Tabs class
#       contains various information panes that can be switched between

from config import *

class Tabs():

    def __init__(self, parent):
        self.parent = parent
        self.notebook = ttk.Notebook(parent)
        self.tabs = []
        self.index = 0
        self.parent.after(500, self.displayloop)

    def place(self, x, y, width, height):
        # fit to current window size
        self.notebook.place(x=x, y=y, width=width, height=height)
        self.x = x # x position
        self.y = y # y position
        self.width = width # width of widget
        self.height = height # height of widget
        for tab in self.tabs:
            tab.place(x+1, y+23, width-4, height-25)
        

    def add_tab(self, child, title):
        self.notebook.add(child, text=title)
        self.tabs.append(child)
        self.notebook.bind_all("<<NotebookTabChanged>>", self.switch)

    def switch(self, event):
        self.index = event.widget.index("current")
        for i in range(0,len(self.tabs)):
            if i != self.index:
                self.tabs[i].hide()
            else:
                self.tabs[i].show()

    def displayloop(self):
        self.tabs[self.index].refresh()
        self.parent.after(30, self.displayloop)

    def reset(self):
        for tab in self.tabs:
            tab.reset()

    def destroy(self):
        self.notebook.destroy()
