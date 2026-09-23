    @Appender(_index_shared_docs["get_loc"])
    def get_loc(self, key, method=None, tolerance=None):
        try:
            if np.all(np.isnan(key)) or is_bool(key):
                nan_idxs = self._nan_idxs
                try:
                    return nan_idxs.item()
                except ValueError:
                    if not len(nan_idxs):
                        raise KeyError(key)
                    return nan_idxs
        except (TypeError, NotImplementedError):
            pass
        return super().get_loc(key, method=method, tolerance=tolerance)
