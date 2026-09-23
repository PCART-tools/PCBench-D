    def _str_isupper(self):
        result = pc.utf8_is_upper(self._pa_array)
        return self._result_converter(result)
