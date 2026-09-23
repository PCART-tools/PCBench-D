    @Appender(Index.isin.__doc__)
    def isin(self, values, level=None):
        if level is None:
            values = MultiIndex.from_tuples(values, names=self.names).values
            return algos.isin(self.values, values)
        else:
            num = self._get_level_number(level)
            levs = self.get_level_values(num)

            if levs.size == 0:
                return np.zeros(len(levs), dtype=np.bool_)
            return levs.isin(values)
