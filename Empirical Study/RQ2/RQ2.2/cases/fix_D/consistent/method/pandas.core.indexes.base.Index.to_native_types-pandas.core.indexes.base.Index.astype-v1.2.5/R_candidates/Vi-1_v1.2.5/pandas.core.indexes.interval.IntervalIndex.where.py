    @Appender(Index.where.__doc__)
    def where(self, cond, other=None):
        if other is None:
            other = self._na_value
        values = np.where(cond, self._values, other)
        result = IntervalArray(values)
        return type(self)._simple_new(result, name=self.name)
