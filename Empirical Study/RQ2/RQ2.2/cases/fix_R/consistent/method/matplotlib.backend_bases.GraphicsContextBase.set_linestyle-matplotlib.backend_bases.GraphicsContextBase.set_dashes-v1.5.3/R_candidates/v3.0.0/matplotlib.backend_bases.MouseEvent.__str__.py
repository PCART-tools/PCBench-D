    def __str__(self):
        return ("MPL MouseEvent: xy=(%d,%d) xydata=(%s,%s) button=%s " +
                "dblclick=%s inaxes=%s") % (self.x, self.y, self.xdata,
                                            self.ydata, self.button,
                                            self.dblclick, self.inaxes)
