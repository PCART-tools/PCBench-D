    def _str_isdigit(self):
        return type(self)(pc.utf8_is_digit(self._data))
