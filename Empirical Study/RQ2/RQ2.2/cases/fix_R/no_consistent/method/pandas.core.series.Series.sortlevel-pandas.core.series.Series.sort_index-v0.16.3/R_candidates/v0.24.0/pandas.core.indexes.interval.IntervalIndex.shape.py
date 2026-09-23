    @property
    def shape(self):
        # Avoid materializing ndarray[Interval]
        return self._data.shape
