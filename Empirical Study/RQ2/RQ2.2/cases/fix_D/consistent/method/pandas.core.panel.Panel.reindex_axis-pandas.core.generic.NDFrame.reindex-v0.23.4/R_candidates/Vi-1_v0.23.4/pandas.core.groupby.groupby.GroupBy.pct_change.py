    @Substitution(name='groupby')
    @Appender(_doc_template)
    def pct_change(self, periods=1, fill_method='pad', limit=None, freq=None,
                   axis=0):
        """Calcuate pct_change of each value to previous entry in group"""
        if freq is not None or axis != 0:
            return self.apply(lambda x: x.pct_change(periods=periods,
                                                     fill_method=fill_method,
                                                     limit=limit, freq=freq,
                                                     axis=axis))

        filled = getattr(self, fill_method)(limit=limit).drop(
            self.grouper.names, axis=1)
        shifted = filled.shift(periods=periods, freq=freq)

        return (filled / shifted) - 1
