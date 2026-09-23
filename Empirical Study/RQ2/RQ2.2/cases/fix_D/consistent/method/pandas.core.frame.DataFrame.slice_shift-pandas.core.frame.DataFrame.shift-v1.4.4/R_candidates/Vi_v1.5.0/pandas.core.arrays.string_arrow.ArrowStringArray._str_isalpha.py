    def _str_isalpha(self):
        result = pc.utf8_is_alpha(self._data)
        return BooleanDtype().__from_arrow__(result)
