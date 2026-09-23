    def _str_isdecimal(self):
        result = pc.utf8_is_decimal(self._data)
        return BooleanDtype().__from_arrow__(result)
