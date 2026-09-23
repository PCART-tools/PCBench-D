    def _str_isdigit(self):
        result = pc.utf8_is_digit(self._pa_array)
        return self._result_converter(result)
