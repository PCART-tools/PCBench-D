    def get_loc(self, key):
        try:
            if np.all(np.isnan(key)):
                try:
                    return self._nan_idxs.item()
                except ValueError:
                    return self._nan_idxs
        except (TypeError, NotImplementedError):
            pass
        return super(Float64Index, self).get_loc(key)
