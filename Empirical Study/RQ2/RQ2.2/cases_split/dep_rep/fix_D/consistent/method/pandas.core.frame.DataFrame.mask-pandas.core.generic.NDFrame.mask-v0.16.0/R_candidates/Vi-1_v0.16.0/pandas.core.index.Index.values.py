    @property
    def values(self):
        """ return the underlying data as an ndarray """
        return self._data.view(np.ndarray)
