    @staticmethod
    def axisinfo(unit, axis):
        # docstring inherited
        majloc = date_ticker.AutoDateLocator()
        majfmt = date_ticker.AutoDateFormatter(majloc)
        return units.AxisInfo(majloc=majloc, majfmt=majfmt, label=unit)
