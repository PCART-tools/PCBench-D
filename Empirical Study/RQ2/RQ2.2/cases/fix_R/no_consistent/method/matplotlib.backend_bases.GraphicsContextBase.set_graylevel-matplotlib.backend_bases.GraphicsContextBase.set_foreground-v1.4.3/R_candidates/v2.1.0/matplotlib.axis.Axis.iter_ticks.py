    def iter_ticks(self):
        """
        Iterate through all of the major and minor ticks.
        """
        majorLocs = self.major.locator()
        majorTicks = self.get_major_ticks(len(majorLocs))
        self.major.formatter.set_locs(majorLocs)
        majorLabels = [self.major.formatter(val, i)
                       for i, val in enumerate(majorLocs)]

        minorLocs = self.minor.locator()
        minorTicks = self.get_minor_ticks(len(minorLocs))
        self.minor.formatter.set_locs(minorLocs)
        minorLabels = [self.minor.formatter(val, i)
                       for i, val in enumerate(minorLocs)]

        major_minor = [
            (majorTicks, majorLocs, majorLabels),
            (minorTicks, minorLocs, minorLabels)]

        for group in major_minor:
            for tick in zip(*group):
                yield tick
