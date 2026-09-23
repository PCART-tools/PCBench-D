    def _str_isupper(self):
        result = pc.utf8_is_upper(self._data)
        return BooleanDtype().__from_arrow__(result)
