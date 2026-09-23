    @staticmethod
    def axisinfo(unit, axis):
        majloc = StrCategoryLocator(axis.unit_data.locs)
        majfmt = StrCategoryFormatter(axis.unit_data.seq)
        return units.AxisInfo(majloc=majloc, majfmt=majfmt)
