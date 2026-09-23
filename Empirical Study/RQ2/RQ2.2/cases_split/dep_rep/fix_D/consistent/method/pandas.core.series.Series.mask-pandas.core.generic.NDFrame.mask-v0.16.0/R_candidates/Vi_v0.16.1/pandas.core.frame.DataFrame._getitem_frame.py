    def _getitem_frame(self, key):
        if key.values.dtype != np.bool_:
            raise ValueError('Must pass DataFrame with boolean values only')
        return self.where(key)
