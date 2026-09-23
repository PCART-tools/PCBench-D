    def _str_islower(self):
        result = pc.utf8_is_lower(self._pa_array)
        return self._result_converter(result)
