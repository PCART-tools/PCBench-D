    def searchsorted(self, value, side="left", sorter=None) -> np.ndarray:
        # overriding IndexOpsMixin improves performance GH#38083
        return self._data.searchsorted(value, side=side, sorter=sorter)
