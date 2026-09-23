    @property
    def groupings(self):
        from pandas.core.groupby.grouper import Grouping

        return [
            Grouping(lvl, lvl, in_axis=False, level=None, name=name)
            for lvl, name in zip(self.levels, self.names)
        ]
