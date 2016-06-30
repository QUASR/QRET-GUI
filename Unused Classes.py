# Controlcentre class: used to send commands to flight computer
class CommandCenter():

    def __init__(self, parent, serialmonitor):
        # affiliate other objects
        self.parent = parent
        self.serialmonitor = serialmonitor
        # set mode
        self.mode = stage
        self.override = IntVar(0)
        # create buttons
        self.resetbutton = Button(parent, text="Reset Device", font=getfont(12), state=DISABLED, command=self.reset)
        self.testbutton = Button(parent, text="Diagnostic Test", font=getfont(12), state=DISABLED, command=self.test)
        self.deploy1button = Button(parent, text="Deploy Payload", font=getfont(12), state=DISABLED, command=self.deploy1)
        self.deploy2button = Button(parent, text="Deploy Parchute", font=getfont(12), state=DISABLED, command=self.deploy2)
        self.senddatabutton = Button(parent, text="Get Flight Data", font=getfont(12), state=DISABLED, command=self.senddata)
        self.overridebutton = Checkbutton(parent, text="Override", font=getfont(12), bg='white', activebackground='white', variable=self.override, command=self.updatemode)

    def place(self, x, y, width, height):
        # fit to current window size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # place buttons
        self.resetbutton.place(x=x, y=y, width=150-bw, height=40)
        self.testbutton.place(x=x+150, y=y, width=150-bw, height=40)
        self.deploy1button.place(x=x, y=y+40+bw, width=150-bw, height=40)
        self.deploy2button.place(x=x+150, y=y+40+bw, width=150-bw, height=40)
        self.senddatabutton.place(x=x, y=y+80+2*bw, width=150-bw, height=40)
        self.overridebutton.place(x=x+175-bw/2, y=y+90+2*bw, width=100, height=20)

    def reset(self):
        print("Placeholder")

    def test(self):
        print("Placeholder")

    def deploy1(self):
        print("Placeholder")

    def deploy2(self):
        print("Placeholder")

    def senddata(self):
        print("Placeholder")

    def updatemode(self, *mode):
        if mode:
            # change mode/stage
            global stage
            self.mode = mode
            stage = mode
        # enable/disable buttons depending on stage
        if not self.override.get():
            if self.mode in ('a','f'): # pre-authentication, secondary descent
                self.resetbutton.configure(state=DISABLED)
                self.testbutton.configure(state=DISABLED)
                self.deploy1button.configure(state=DISABLED)
                self.deploy2button.configure(state=DISABLED)
                self.senddatabutton.configure(state=DISABLED)
            elif self.mode in ('b','c'): # after authentication, before launch
                self.resetbutton.configure(state=NORMAL)
                self.testbutton.configure(state=NORMAL)
                self.deploy1button.configure(state=DISABLED)
                self.deploy2button.configure(state=DISABLED)
                self.senddatabutton.configure(state=DISABLED)
            elif self.mode == 'd': # after launch, before payload deployment
                self.resetbutton.configure(state=DISABLED)
                self.testbutton.configure(state=DISABLED)
                self.deploy1button.configure(state=NORMAL)
                self.deploy2button.configure(state=DISABLED)
                self.senddatabutton.configure(state=DISABLED)
            elif self.mode == 'e': # between two deployments
                self.resetbutton.configure(state=DISABLED)
                self.testbutton.configure(state=DISABLED)
                self.deploy1button.configure(state=DISABLED)
                self.deploy2button.configure(state=NORMAL)
                self.senddatabutton.configure(state=DISABLED)
            elif self.mode == 'g': # after landing
                self.resetbutton.configure(state=DISABLED)
                self.testbutton.configure(state=DISABLED)
                self.deploy1button.configure(state=DISABLED)
                self.deploy2button.configure(state=DISABLED)
                self.senddatabutton.configure(state=NORMAL)
            else:
                raise Exception("mode '",str(self.mode),"' is undefined")
        else: # enable all buttons when override is enabled
            self.resetbutton.configure(state=NORMAL)
            self.testbutton.configure(state=NORMAL)
            self.deploy1button.configure(state=NORMAL)
            self.deploy2button.configure(state=NORMAL)
            self.senddatabutton.configure(state=NORMAL)
                

    def destroy(self):
        self.resetbutton.destroy()
        self.testbutton.destroy()
        self.deploy1button.destroy()
        self.deploy2button.destroy()
        self.senddatabutton.destroy()
        self.overridebutton.destroy()
