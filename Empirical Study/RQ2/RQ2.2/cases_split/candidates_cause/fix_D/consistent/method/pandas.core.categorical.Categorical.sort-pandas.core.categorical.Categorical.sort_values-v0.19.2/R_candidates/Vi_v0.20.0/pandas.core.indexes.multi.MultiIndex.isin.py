    @Appender(Index.isin.__doc__)
    def isin(self, values, level=None):
        if level is None:
            return algos.isin(self.values,
                              MultiIndex.from_tuples(values).values)
        else:
            num = self._get_level_number(level)
            levs = self.levels[num]
            labs = self.labels[num]

            sought_labels = levs.isin(values).nonzero()[0]
            if levs.size == 0:
                return np.zeros(len(labs), dtype=np.bool_)
            else:
                return np.lib.arraysetops.in1d(labs, sought_labels)
