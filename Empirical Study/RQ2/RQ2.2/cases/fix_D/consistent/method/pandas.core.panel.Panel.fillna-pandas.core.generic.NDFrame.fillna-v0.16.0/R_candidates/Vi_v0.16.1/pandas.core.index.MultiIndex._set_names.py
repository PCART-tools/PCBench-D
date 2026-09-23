    def _set_names(self, names, level=None, validate=True):
        """
        sets names on levels. WARNING: mutates!

        Note that you generally want to set this *after* changing levels, so
        that it only acts on copies
        """

        names = list(names)

        if validate and level is not None and len(names) != len(level):
            raise ValueError('Length of names must match length of level.')
        if validate and level is None and len(names) != self.nlevels:
            raise ValueError(
                'Length of names must match number of levels in MultiIndex.')

        if level is None:
            level = range(self.nlevels)
        else:
            level = [self._get_level_number(l) for l in level]

        # set the name
        for l, name in zip(level, names):
            self.levels[l].rename(name, inplace=True)
