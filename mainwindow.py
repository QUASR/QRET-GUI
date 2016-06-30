#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   MainWindow class
#       main window that houses all widgets

from config import *

class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.menubar = Menu(parent)
        
        self.initUI()
        self.widgets = ()
        
    def initUI(self):
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Export", command=self.export_file)
        self.filemenu.add_command(label="Reset data", command=self.reset)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)
        self.parent.geometry(resolution)
        self.parent.title("QRET Rocket GUI")
        self.pack(fill=tkinter.BOTH, expand=1)

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

    def open_file(self):
        to_open = filedialog.askopenfilename(parent=self.parent)
        if to_open is not None:
            self.reset()
            

    def export_file(self):
        print("Export")

    def reset(self):
        for widget in self.widgets:
            widget.reset()

    def destroy(self):
        for widget in self.widgets:
            widget.destroy()
