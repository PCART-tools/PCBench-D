    def unique(self) -> Self:
        new_data = unique(self._ndarray)
        return self._from_backing_data(new_data)
