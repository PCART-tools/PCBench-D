    @Appender(Index.isin.__doc__)
    def isin(self, values, level=None):
        if level is None:
            values = MultiIndex.from_tuples(values, names=self.names).values
            return algos.isin(self.values, values)
        else:
            num = self._get_level_number(level)
            levs = self.levels[num]
            level_codes = self.codes[num]

            sought_labels = levs.isin(values).nonzero()[0]
            if levs.size == 0:
                return np.zeros(len(level_codes), dtype=np.bool_)
            else:
                return np.lib.arraysetops.in1d(level_codes, sought_labels)
