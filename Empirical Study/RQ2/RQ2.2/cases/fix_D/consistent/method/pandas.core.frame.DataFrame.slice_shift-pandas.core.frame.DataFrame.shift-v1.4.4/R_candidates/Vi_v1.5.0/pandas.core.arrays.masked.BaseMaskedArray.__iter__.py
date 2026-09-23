    def __iter__(self):
        if self.ndim == 1:
            for i in range(len(self)):
                if self._mask[i]:
                    yield self.dtype.na_value
                else:
                    yield self._data[i]
        else:
            for i in range(len(self)):
                yield self[i]
