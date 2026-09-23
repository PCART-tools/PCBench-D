    def __str__(self):
        return "AxesImage(%g,%g;%gx%g)" % tuple(self.axes.bbox.bounds)
