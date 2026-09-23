    @copy(str_cat)
    def cat(self, others=None, sep=None, na_rep=None):
        data = self._orig if self._is_categorical else self._data
        result = str_cat(data, others=others, sep=sep, na_rep=na_rep)
        return self._wrap_result(result, use_codes=(not self._is_categorical))
