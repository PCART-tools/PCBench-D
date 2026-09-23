    @property
    def groupings(self) -> list[grouper.Grouping]:
        lev = self.binlabels
        ping = grouper.Grouping(lev, lev, in_axis=False, level=None)
        return [ping]
