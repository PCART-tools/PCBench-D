    def _str_isalnum(self):
        return type(self)(pc.utf8_is_alnum(self._pa_array))
