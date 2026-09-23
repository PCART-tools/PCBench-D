    def _str_isalnum(self):
        result = pc.utf8_is_alnum(self._pa_array)
        return self._result_converter(result)
