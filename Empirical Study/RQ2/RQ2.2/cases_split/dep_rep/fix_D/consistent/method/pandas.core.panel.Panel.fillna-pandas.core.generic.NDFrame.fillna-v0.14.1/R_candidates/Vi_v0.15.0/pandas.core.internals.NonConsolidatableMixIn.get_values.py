    def get_values(self, dtype=None):
        """ need to to_dense myself (and always return a ndim sized object) """
        values = self.values.to_dense()
        if values.ndim == self.ndim - 1:
            values = values.reshape((1,) + values.shape)
        return values
