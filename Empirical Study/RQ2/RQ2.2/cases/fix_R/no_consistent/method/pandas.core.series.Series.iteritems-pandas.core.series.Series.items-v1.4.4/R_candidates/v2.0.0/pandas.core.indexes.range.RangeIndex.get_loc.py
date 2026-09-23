    @doc(Index.get_loc)
    def get_loc(self, key):
        if is_integer(key) or (is_float(key) and key.is_integer()):
            new_key = int(key)
            try:
                return self._range.index(new_key)
            except ValueError as err:
                raise KeyError(key) from err
        self._check_indexing_error(key)
        raise KeyError(key)
