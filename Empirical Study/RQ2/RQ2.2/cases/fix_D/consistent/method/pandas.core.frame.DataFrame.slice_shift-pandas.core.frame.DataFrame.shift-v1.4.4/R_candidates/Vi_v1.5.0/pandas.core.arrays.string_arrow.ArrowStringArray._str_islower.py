    def _str_islower(self):
        result = pc.utf8_is_lower(self._data)
        return BooleanDtype().__from_arrow__(result)
