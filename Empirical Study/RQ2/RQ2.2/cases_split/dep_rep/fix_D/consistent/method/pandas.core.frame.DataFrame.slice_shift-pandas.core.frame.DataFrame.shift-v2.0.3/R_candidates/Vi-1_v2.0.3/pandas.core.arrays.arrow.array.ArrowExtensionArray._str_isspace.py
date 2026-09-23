    def _str_isspace(self):
        return type(self)(pc.utf8_is_space(self._data))
