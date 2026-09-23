    @property
    def groupings(self) -> list[grouper.Grouping]:
        lev = self.binlabels
        codes = self.group_info[0]
        labels = lev.take(codes)
        ping = grouper.Grouping(
            labels, labels, in_axis=False, level=None, uniques=lev._values
        )
        return [ping]
