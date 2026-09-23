    @property
    def groupings(self):
        return [Grouping(lvl, lvl, in_axis=False, level=None, name=name)
                for lvl, name in zip(self.levels, self.names)]
