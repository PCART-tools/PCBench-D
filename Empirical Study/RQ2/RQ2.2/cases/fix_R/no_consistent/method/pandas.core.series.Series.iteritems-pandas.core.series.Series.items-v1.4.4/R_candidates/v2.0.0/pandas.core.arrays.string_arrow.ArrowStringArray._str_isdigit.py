    def _str_isdigit(self):
        result = pc.utf8_is_digit(self._data)
        return BooleanDtype().__from_arrow__(result)
