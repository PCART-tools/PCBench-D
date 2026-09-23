    @Substitution(klass='DatetimeIndex')
    @Appender(_shared_docs['searchsorted'])
    def searchsorted(self, value, side='left', sorter=None):
        if isinstance(value, (np.ndarray, Index)):
            value = np.array(value, dtype=_NS_DTYPE, copy=False)
        else:
            value = _to_M8(value, tz=self.tz)

        return self.values.searchsorted(value, side=side)
