    @doc(Index.get_loc)
    def get_loc(self, key, method=None, tolerance=None):
        if is_bool(key):
            # Catch this to avoid accidentally casting to 1.0
            raise KeyError(key)

        if is_float(key) and np.isnan(key):
            nan_idxs = self._nan_idxs
            if not len(nan_idxs):
                raise KeyError(key)
            elif len(nan_idxs) == 1:
                return nan_idxs[0]
            return nan_idxs

        return super().get_loc(key, method=method, tolerance=tolerance)
