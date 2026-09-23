    def _str_islower(self):
        return type(self)(pc.utf8_is_lower(self._pa_array))
