    def _str_isalpha(self):
        return type(self)(pc.utf8_is_alpha(self._pa_array))
