    def _str_len(self):
        result = pc.utf8_length(self._pa_array).to_numpy()
        return self._convert_int_dtype(result)
