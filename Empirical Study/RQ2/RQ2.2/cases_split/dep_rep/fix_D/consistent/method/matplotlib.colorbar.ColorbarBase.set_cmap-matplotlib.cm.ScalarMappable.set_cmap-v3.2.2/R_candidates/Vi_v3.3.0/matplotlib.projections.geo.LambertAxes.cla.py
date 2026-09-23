    def cla(self):
        GeoAxes.cla(self)
        self.yaxis.set_major_formatter(NullFormatter())
