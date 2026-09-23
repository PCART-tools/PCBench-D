    @property
    def size(self):
        # Avoid materializing ndarray[Interval]
        return self._data.size
