    def _getitem_frame(self, key):
        if key.values.size and not is_bool_dtype(key.values):
            raise ValueError('Must pass DataFrame with boolean values only')
        return self.where(key)
