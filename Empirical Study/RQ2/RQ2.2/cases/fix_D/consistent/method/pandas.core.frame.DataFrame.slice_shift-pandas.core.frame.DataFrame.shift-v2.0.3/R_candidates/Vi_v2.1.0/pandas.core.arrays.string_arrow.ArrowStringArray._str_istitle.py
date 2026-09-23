    def _str_istitle(self):
        result = pc.utf8_is_title(self._pa_array)
        return self._result_converter(result)
