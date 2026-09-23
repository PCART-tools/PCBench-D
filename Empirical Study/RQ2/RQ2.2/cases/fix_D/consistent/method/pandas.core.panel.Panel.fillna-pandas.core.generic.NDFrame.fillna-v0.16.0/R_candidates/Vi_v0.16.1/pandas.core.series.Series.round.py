    @Appender(np.ndarray.round.__doc__)
    def round(self, decimals=0, out=None):
        """

        """
        result = _values_from_object(self).round(decimals, out=out)
        if out is None:
            result = self._constructor(result,
                                       index=self.index).__finalize__(self)

        return result
