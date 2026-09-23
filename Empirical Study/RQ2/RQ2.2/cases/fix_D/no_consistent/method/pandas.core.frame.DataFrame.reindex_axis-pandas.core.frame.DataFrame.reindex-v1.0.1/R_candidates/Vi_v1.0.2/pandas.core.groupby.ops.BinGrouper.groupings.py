    @property
    def groupings(self) -> "List[grouper.Grouping]":
        return [
            grouper.Grouping(lvl, lvl, in_axis=False, level=None, name=name)
            for lvl, name in zip(self.levels, self.names)
        ]
