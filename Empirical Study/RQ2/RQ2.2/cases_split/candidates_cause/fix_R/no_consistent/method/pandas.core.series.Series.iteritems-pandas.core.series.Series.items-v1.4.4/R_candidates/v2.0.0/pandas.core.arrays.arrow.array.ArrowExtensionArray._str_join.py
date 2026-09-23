    def _str_join(self, sep: str):
        return type(self)(pc.binary_join(self._data, sep))
