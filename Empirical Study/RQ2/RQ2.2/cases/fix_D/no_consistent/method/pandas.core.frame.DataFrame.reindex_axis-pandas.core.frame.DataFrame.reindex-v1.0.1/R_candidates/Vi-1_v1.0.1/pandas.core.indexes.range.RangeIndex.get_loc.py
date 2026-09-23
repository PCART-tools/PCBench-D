    @Appender(_index_shared_docs["get_loc"])
    def get_loc(self, key, method=None, tolerance=None):
        if is_integer(key) and method is None and tolerance is None:
            new_key = int(key)
            try:
                return self._range.index(new_key)
            except ValueError:
                raise KeyError(key)
        return super().get_loc(key, method=method, tolerance=tolerance)
