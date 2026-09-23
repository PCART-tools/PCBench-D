    def _str_isnumeric(self):
        result = pc.utf8_is_numeric(self._data)
        return BooleanDtype().__from_arrow__(result)
