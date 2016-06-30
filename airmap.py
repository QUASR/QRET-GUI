#   QUASR Rocket GUI

#   Eric Donders
#   January 19, 2016

#   Map class
#       displays an aerial image of the launch area

from config import *

class Map():

    def __init__(self, parent, imagefile, tlc_coords, brc_coords, w0, h0, zoom = 1):
        self.parent = parent
        self.base_image = PhotoImage(file = imagefile)
        self.image = self.base_image
        self.tlc_coords = tlc_coords
        self.brc_coords = brc_coords
        self.ns_span = self.tlc_coords[0] - self.brc_coords[0]
        self.ew_span = self.tlc_coords[1] - self.brc_coords[1]
        self.w0 = w0
        self.h0 = h0
        self.width = w0
        self.height = h0
        self.zoom = zoom

    def resize(self, direction):
        self.zoom = self.zoom + direction
        if self.zoom < 1:
            self.zoom = 1
        elif self.zoom > 4:
            self.zoom = 4
        self.width = self.w0 / self.zoom
        self.height = self.h0 / self.zoom
        self.image = self.base_image.subsample(self.zoom, self.zoom)

    def destroy(self):
        self.image.destroy()
