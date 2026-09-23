    def set_default_intervals(self):
        # docstring inherited
        xmin, xmax = 0., 1.
        dataMutated = self.axes.dataLim.mutatedx()
        viewMutated = self.axes.viewLim.mutatedx()
        if not dataMutated or not viewMutated:
            if self.converter is not None:
                info = self.converter.axisinfo(self.units, self)
                if info.default_limits is not None:
                    valmin, valmax = info.default_limits
                    xmin = self.converter.convert(valmin, self.units, self)
                    xmax = self.converter.convert(valmax, self.units, self)
            if not dataMutated:
                self.axes.dataLim.intervalx = xmin, xmax
            if not viewMutated:
                self.axes.viewLim.intervalx = xmin, xmax
        self.stale = True
