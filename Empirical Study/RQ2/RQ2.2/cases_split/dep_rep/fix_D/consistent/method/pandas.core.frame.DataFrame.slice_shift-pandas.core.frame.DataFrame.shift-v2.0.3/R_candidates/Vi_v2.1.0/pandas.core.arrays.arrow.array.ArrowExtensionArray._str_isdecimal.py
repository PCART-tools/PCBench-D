    def _str_isdecimal(self):
        return type(self)(pc.utf8_is_decimal(self._pa_array))
