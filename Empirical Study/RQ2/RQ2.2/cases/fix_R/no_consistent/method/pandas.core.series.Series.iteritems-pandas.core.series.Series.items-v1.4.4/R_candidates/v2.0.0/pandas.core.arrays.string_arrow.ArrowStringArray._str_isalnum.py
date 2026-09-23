    def _str_isalnum(self):
        result = pc.utf8_is_alnum(self._data)
        return BooleanDtype().__from_arrow__(result)
