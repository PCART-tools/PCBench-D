    def _str_isdecimal(self):
        result = pc.utf8_is_decimal(self._pa_array)
        return self._result_converter(result)
