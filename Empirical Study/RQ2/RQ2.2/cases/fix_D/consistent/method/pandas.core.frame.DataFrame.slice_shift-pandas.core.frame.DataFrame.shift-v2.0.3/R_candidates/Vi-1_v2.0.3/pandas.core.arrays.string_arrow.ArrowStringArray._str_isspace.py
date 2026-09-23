    def _str_isspace(self):
        result = pc.utf8_is_space(self._data)
        return BooleanDtype().__from_arrow__(result)
