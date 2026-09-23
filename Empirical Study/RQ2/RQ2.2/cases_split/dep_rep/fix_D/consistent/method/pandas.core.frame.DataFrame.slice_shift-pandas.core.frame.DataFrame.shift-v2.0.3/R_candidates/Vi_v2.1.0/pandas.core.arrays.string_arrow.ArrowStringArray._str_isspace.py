    def _str_isspace(self):
        result = pc.utf8_is_space(self._pa_array)
        return self._result_converter(result)
