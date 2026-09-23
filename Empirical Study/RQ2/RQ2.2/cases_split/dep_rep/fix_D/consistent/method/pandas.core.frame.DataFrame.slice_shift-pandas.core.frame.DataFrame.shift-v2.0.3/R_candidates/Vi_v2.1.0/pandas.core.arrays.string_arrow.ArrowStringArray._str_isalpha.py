    def _str_isalpha(self):
        result = pc.utf8_is_alpha(self._pa_array)
        return self._result_converter(result)
