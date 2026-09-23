    @fill_value.setter
    def fill_value(self, value) -> None:
        self._dtype = SparseDtype(self.dtype.subtype, value)
