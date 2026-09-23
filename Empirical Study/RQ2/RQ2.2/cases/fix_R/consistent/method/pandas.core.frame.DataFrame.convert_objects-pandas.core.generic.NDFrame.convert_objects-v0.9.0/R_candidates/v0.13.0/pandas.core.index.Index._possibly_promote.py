    def _possibly_promote(self, other):
        # A hack, but it works
        from pandas.tseries.index import DatetimeIndex
        if self.inferred_type == 'date' and isinstance(other, DatetimeIndex):
            return DatetimeIndex(self), other
        return self, other
