    def set_data_interval(self, vmin, vmax, ignore=False):
        'set the axis data limits'
        if ignore:
            self.axes.dataLim.intervaly = vmin, vmax
        else:
            Vmin, Vmax = self.get_data_interval()
            self.axes.dataLim.intervaly = min(vmin, Vmin), max(vmax, Vmax)
        self.stale = True
