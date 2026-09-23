    def _str_isnumeric(self):
        result = pc.utf8_is_numeric(self._pa_array)
        return self._result_converter(result)
