    def _set_names(self, values, validate=True):
        """
        sets names on levels. WARNING: mutates!

        Note that you generally want to set this *after* changing levels, so
        that it only acts on copies"""
        values = list(values)
        if validate and len(values) != self.nlevels:
            raise ValueError('Length of names must match length of levels')
        # set the name
        for name, level in zip(values, self.levels):
            level.rename(name, inplace=True)
