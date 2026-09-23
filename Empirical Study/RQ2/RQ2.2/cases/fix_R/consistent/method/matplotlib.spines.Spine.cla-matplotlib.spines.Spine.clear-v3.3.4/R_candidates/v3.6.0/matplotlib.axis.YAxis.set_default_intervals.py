    def set_default_intervals(self):
        # docstring inherited
        # only change view if dataLim has not changed and user has
        # not changed the view:
        if (not self.axes.dataLim.mutatedy() and
                not self.axes.viewLim.mutatedy()):
            if self.converter is not None:
                info = self.converter.axisinfo(self.units, self)
                if info.default_limits is not None:
                    ymin, ymax = self.convert_units(info.default_limits)
                    self.axes.viewLim.intervaly = ymin, ymax
        self.stale = True
