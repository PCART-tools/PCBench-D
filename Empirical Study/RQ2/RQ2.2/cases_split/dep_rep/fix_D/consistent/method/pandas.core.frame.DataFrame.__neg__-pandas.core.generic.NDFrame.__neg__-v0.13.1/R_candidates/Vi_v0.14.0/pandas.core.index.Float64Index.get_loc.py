    def get_loc(self, key):
        if np.isnan(key):
            try:
                return self._nan_idxs.item()
            except ValueError:
                return self._nan_idxs
        return super(Float64Index, self).get_loc(key)
