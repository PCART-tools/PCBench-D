    def _str_isnumeric(self):
        return type(self)(pc.utf8_is_numeric(self._pa_array))
