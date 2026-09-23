    def set_default_intervals(self):
        # docstring inherited
        ymin, ymax = 0., 1.
        dataMutated = self.axes.dataLim.mutatedy()
        viewMutated = self.axes.viewLim.mutatedy()
        if not dataMutated or not viewMutated:
            if self.converter is not None:
                info = self.converter.axisinfo(self.units, self)
                if info.default_limits is not None:
                    valmin, valmax = info.default_limits
                    ymin = self.converter.convert(valmin, self.units, self)
                    ymax = self.converter.convert(valmax, self.units, self)
            if not dataMutated:
                self.axes.dataLim.intervaly = ymin, ymax
            if not viewMutated:
                self.axes.viewLim.intervaly = ymin, ymax
        self.stale = True
