    @doc(Int64Index.get_loc)
    def get_loc(self, key, method=None, tolerance=None):
        if method is None and tolerance is None:
            if is_integer(key) or (is_float(key) and key.is_integer()):
                new_key = int(key)
                try:
                    return self._range.index(new_key)
                except ValueError as err:
                    raise KeyError(key) from err
            self._check_indexing_error(key)
            raise KeyError(key)
        return super().get_loc(key, method=method, tolerance=tolerance)
