    def _str_swapcase(self):
        return type(self)(pc.utf8_swapcase(self._pa_array))
