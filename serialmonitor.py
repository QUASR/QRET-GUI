#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   SerialMonitor class
#       deals with serial communication and message panel

from config import *

class SerialMonitor():

    def __init__(self, parent, hplot, mplot, plotwindow, meter):
        "SerialMonitor constructor"
        self.scrollbar = Scrollbar(parent)
        self.listbox = Listbox(parent, bg='white', yscrollcommand=self.scrollbar.set, font=getfont(10))
        self.temptext = Text(parent, font=getfont(12), bd=0)
        self.scrollbar.config(command=self.listbox.yview)
        self.parent = parent
        self.hplot = hplot
        self.mplot = mplot
        self.plotwindow = plotwindow

        self.meter = meter
        self.temp = "-"
        
        self.t0 = 0 # replace later
        timestamp = str(time.asctime(time.localtime(time.time())))
        str_ = "Started " + timestamp
        self.listbox.insert(tkinter.END, str_)
        logfile = "Logs/QRET_Log " + timestamp.replace(':', '-') + ".txt"
        self.file = open(logfile, 'a')
        self.file.write(str_+"\n\r")

        self.payloadserial = serial.Serial(baudrate=9600)
        self.rocketserial = serial.Serial(baudrate=9600)
        
        self.log("Trying to connect to devices")
        self.payloadserialopen = False
        self.payloadauthenticated = False
        self.rocketserialopen = False
        self.rocketauthenticated = False
        self.rocketbuffer = ""

        self.accelscale = 16 # G at 32767
        self.gyroscale = 1000 # degrees/sec at 32767

        # Set initial "guess" serial ports.
        try:
            self.payloadserial.port = 1
            self.rocketserial.port = 4
            self.scan_ports()
        except ValueError:
            # Different computers use different syntax for COM ports
            self.payloadserial.port = "COM11"
            self.rocketserial.port = "COM4"
            self.scan_ports_alt()
        
    def place(self, x, y, width, height):
        "Moves or resizes object to new geometry"
        self.scrollbar.place(x=x+width-16, y=y, width=16, height=height-20-bw)
        self.listbox.place(x=x, y=y, width=width-16, height=height-20-bw)
        self.meter.place(x=x+130, y=y+height-20, width=width-130, height=20)
        self.temptext.place(x=x, y=y+height-20, width=130, height=20)
        self.x = x
        self.y = y
        self.w = width
        self.h = height


    def scan_ports(self):
        "Scans through serial ports, looking for signals from payload and rocket"
        #print("scan_ports")
        force_exit = False
        if not self.payloadserialopen:
            try:
                self.payloadserial.open()
                self.payloadserialopen = True
            except Exception as e:
                try:
                    self.payloadserial.port = self.payloadserial.port % 15 + 1
                except:
                    pass
        elif not self.payloadauthenticated:
            while self.payloadserial.inWaiting() > 0:
                first = self.payloadserial.read().decode()
                if first == "$":
                    self.payloadauthenticated = True
            if not self.payloadauthenticated:
                try:
                    self.payloadserialopen = False
                    self.payloadserial.port = self.payloadserial.port % 15 + 1
                except:
                    pass
            else:
                self.message("Connected to payload on COM"+str(self.payloadserial.port + 1))
                self.receive_pl()
                
        if not self.rocketserialopen:
            try:
                self.rocketserial.open()
                self.rocketserialopen = True
            except Exception as e:
                self.rocketserial.port = self.rocketserial.port % 15 + 1
                if str(e)[:5] == "'int'":
                    self.payloadserial.port = "COM" + str(self.payloadserial.port + 1)
                    self.rocketserial.port = "COM" + str(self.rocketserial.port + 1)
                    force_exit = True
                    self.scan_ports_alt()
        elif not self.rocketauthenticated:
            while self.rocketserial.inWaiting() > 0:
                try:
                    first = self.rocketserial.read().decode()
                    if first == "%":
                        self.rocketauthenticated = True
                except:
                    pass
            if not self.rocketauthenticated:
                try:
                    self.rocketserialopen = False
                    self.rocketserial.port = self.rocketserial.port % 15 + 1
                except:
                    pass
            else:
                self.message("Connected to rocket on COM"+str(self.rocketserial.port + 1))
                self.receive_rocket()

        if not (self.rocketauthenticated or force_exit): ####################### update
            self.parent.after(90, self.scan_ports)

    def scan_ports_alt(self):
        "Alternate scanning function for different port name"
        if not self.payloadserialopen:
            try:
                self.payloadserial.open()
                self.payloadserialopen = True
            except:
                self.payloadserial.port = "COM" + str(int(self.payloadserial.port[3:]) % 15 + 1)
        elif not self.payloadauthenticated:
            while self.payloadserial.inWaiting() > 0:
                first = self.payloadserial.read().decode()
                if first == "$":
                    self.payloadauthenticated = True
            if not self.payloadauthenticated:
                try:
                    pass
                    #self.payloadserialopen = False
                    #self.payloadserial.port = "COM" + str(int(self.payloadserial.port[3:]) % 15 + 1)
                except:
                    pass
            else:
                self.message("Connected to payload on COM"+str(int(self.payloadserial.port[3:])))
                self.receive_pl()
                
        if not self.rocketserialopen:
            try:
                self.rocketserial.open()
                self.rocketserialopen = True
            except Exception:
                self.rocketserial.port = "COM" + str(int(self.rocketserial.port[3:]) % 15 + 1)
        elif not self.rocketauthenticated:
            while self.rocketserial.inWaiting() > 0:
                try:
                    first = self.rocketserial.read().decode()
                    if first == "%":
                        self.rocketauthenticated = True
                except:
                    pass
            if not self.rocketauthenticated:
                try:
                    pass
                    #self.rocketserialopen = False
                    #self.rocketserial.port = "COM" + str(int(self.rocketserial.port[3:]) % 15 + 1)
                except:
                    pass
            else:
                self.message("Connected to rocket on COM"+str(int(self.rocketserial.port[3:])))
                self.receive_rocket()

        if not (self.rocketauthenticated and self.payloadauthenticated):
            self.parent.after(90, self.scan_ports_alt)
        else:
            print("finished")
                    
        
    def receive_pl(self):
        "Attempts to read a payload data point from the serial port"
        if not self.payloadauthenticated:
            if self.payloadserial.inWaiting() > 0:
                self.payloadauthenticated = True
                self.message("Payload authenticated")
        else:
            first = self.payloadserial.read().decode()
            if first != "$":
                self.file.write(first)
            elif self.payloadserial.inWaiting() >= 68:
                try:
                    msg = self.payloadserial.read(68).decode()
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
                    if self.t0 == 0:
                        self.t0 = time.clock()
                    tval = time.clock()-self.t0
                    self.hplot.send(tval, altitude,0)
                    self.hplot.draw()
                    self.mplot.send(latitude,longitude,"pl")
                    if self.t0 == 0:
                        self.t0 = time.clock()
                except:
                    pass

        # Repeat every sec
        self.parent.after(90, self.receive_pl)

    def receive_rocket(self):
        "Attempt to read a rocket data point from the serial port"
        self.rocketbuffer = self.rocketbuffer + self.rocketserial.read(self.rocketserial.inWaiting()).decode()
        while len(self.rocketbuffer) > 0 and self.rocketbuffer[0] != "%":
            if self.rocketbuffer.find("%") == -1:
                self.rocketbuffer = ""
            else:
                self.rocketbuffer = self.rocketbuffer[self.rocketbuffer.find("%"):]
                # break
        n=0
        while len(self.rocketbuffer) > 75:
            n = n+1
            index = self.rocketbuffer.find("|")
            if self.rocketbuffer[0] == "%" and index != -1:
                try:
                    index1 = self.rocketbuffer.find(" ",3)
                    tval = float(self.rocketbuffer[2:index1])/1000
                    if self.t0 == 0:
                        self.t0 = time.clock()
                    t = time.clock()-self.t0
                    if self.rocketbuffer[1] == "m":
                        index2 = self.rocketbuffer.find(" ", index1+1)
                        index3 = self.rocketbuffer.find(" ", index2+1)
                        index4 = self.rocketbuffer.find(" ", index3+1)
                        index5 = self.rocketbuffer.find(" ", index4+1)
                        index6 = self.rocketbuffer.find(" ", index5+1)
                        index7 = self.rocketbuffer.find(" ", index6+1)
                        index8 = self.rocketbuffer.find(" ", index7+1)
                        index9 = self.rocketbuffer.find(" ", index8+1)
                        ax = float(self.rocketbuffer[index1:index2]) / 32767 * self.accelscale
                        ay = float(self.rocketbuffer[index2:index3]) / 32767 * self.accelscale
                        az = float(self.rocketbuffer[index3:index4]) / 32767 * self.accelscale
                        gx = float(self.rocketbuffer[index4:index5]) / 32767 * self.gyroscale
                        gy = float(self.rocketbuffer[index5:index6]) / 32767 * self.gyroscale
                        gz = float(self.rocketbuffer[index6:index7]) / 32767 * self.gyroscale
                        mx = float(self.rocketbuffer[index7:index8])
                        my = float(self.rocketbuffer[index8:index9])
                        mz = float(self.rocketbuffer[index9:index])
                        self.plotwindow.accel_plot.send(t, ax, 0)
                        self.plotwindow.accel_plot.send(t, ay, 1)
                        self.plotwindow.accel_plot.send(t, az, 2)
                        self.plotwindow.gyro_plot.send(t, gx, 0)
                        self.plotwindow.gyro_plot.send(t, gy, 1)
                        self.plotwindow.gyro_plot.send(t, gz, 2)
                        self.plotwindow.mag_plot.send(t, mx, 0)
                        self.plotwindow.mag_plot.send(t, my, 1)
                        self.plotwindow.mag_plot.send(t, mz, 2)
                        # designate log values
                        log_list = ("m,",t,',',ax,',',ay,',',az,',',gx,',',gy,',',gz,',',mx,',',my,',',mz)
                    elif self.rocketbuffer[1] == "b":
                        index2 = self.rocketbuffer.find(" ", index1+1)
                        alt = int(self.rocketbuffer[index1:index2])
                        temp = int(self.rocketbuffer[index2:index])
                        self.hplot.send(time.clock()-self.t0, alt, 1)
                        self.send(temp)
                        self.hplot.draw()
                        # designate log values
                        log_list = ("b,",t,',',alt,',',temp)
                    elif self.rocketbuffer[1] == "a":
                        angle = int(self.rocketbuffer[index1:index])
                        self.plotwindow.attitude_plot.send(angle)
                        log_list = ("a,",t,',',angle)
                    elif self.rocketbuffer[1] == "g":
                        try:
                            #print(self.rocketbuffer[:index])
                            index2 = self.rocketbuffer.find(" ", index1+1)
                            latitude =  float(self.rocketbuffer[index1:index1+3]) + float(self.rocketbuffer[index1+3:index2])/60
                            longitude = float(self.rocketbuffer[index2:index2+4]) + float(self.rocketbuffer[index2+4:index])/60
                            self.mplot.send(latitude, longitude, "r")
                            # designate log values
                            log_list = ("g,",t,',',latitude,',',longitude)
                            #print(str(latitude) + " " + str(longitude))
                        except:
                            self.message("Warning! Error reading GPS data: " + str(self.rocketbuffer[:index]))
                            log_list = ("g,E,E")
                    elif self.rocketbuffer[1] == "i":
                        text = self.rocketbuffer[index1:index]
                        self.message(text)
                        log_list = ''
                    else:
                        log_list = ("Undefined value: ",self.rocketbuffer[1])

                    # write data to file
                    if log_list != '':
                        to_log = ''.join(str(entry) for entry in log_list)
                        self.log(to_log)
                                
                    if len(self.rocketbuffer) > 500:
                        self.message("Warning! Serial buffer length: " + str(len(self.rocketbuffer)))
                except Exception as e:
                    self.message("Warning! Exception occurred while parsing rocket data:\r\n" + str(e))
                self.rocketbuffer = self.rocketbuffer[index+1:]
                    
            else:
                break

        # Repeat every n milliseconds
        self.parent.after(5, self.receive_rocket)
        

    def command(self, cmd):
        "UNUSED - Send a command to the payload"
        if self.payloadserialopen and self.authenticated:
            self.payloadserial.write(cmd)

    def message(self, msg):
        "Called to display a message and log it in the log file"
        t = time.localtime(time.time())
        self.listbox.insert(tkinter.END, str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)+" > "+msg)
        self.log(msg)

    def log(self, msg):
        "Writes a message to the log file along with a timestamp"
        t = time.localtime(time.time())
        str_ = str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)+" > "+msg
        self.file.write(str_+"\n\r")

    def setcommandcenter(self, commandcenter):
        "Attaches a commandcenter object to the serialmonitor"
        self.commandcenter = commandcenter

    def send(self, temperature):
        "Called to update the temperature display"
        self.temperature = temperature
        self.temptext.delete(1.0, tkinter.END)
        self.temptext.insert(tkinter.END, str(temperature) + u"\u00b0" + "C")
        self.place(x=self.x, y=self.y, width=self.w, height=self.h)

    def reset(self):
        "Clears all data and refreshes the view"
        self.t0 = 0
        self.hplot.refresh()
        self.send("-")
        self.meter.reset()
        self.listbox.delete(0, tkinter.END)
        str_ = "Started "+str(time.asctime(time.localtime(time.time())))
        self.listbox.insert(tkinter.END, str_)
        self.file.write(str_+"\n\r")
            
    def destroy(self):
        "Called on program close to clean up"
        self.scrollbar.destroy()
        self.listbox.destroy()
        if self.payloadserialopen:
            self.payloadserial.close()
            self.log("Closed payload serial connection")
        if self.rocketserialopen:
            self.rocketserial.close()
            self.log("Closed rocket serial connection")
        self.file.write("\n\r")
        self.file.close()
        print("Closed log file")

