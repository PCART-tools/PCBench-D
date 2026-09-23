    def _str_len(self):
        return type(self)(pc.utf8_length(self._pa_array))
