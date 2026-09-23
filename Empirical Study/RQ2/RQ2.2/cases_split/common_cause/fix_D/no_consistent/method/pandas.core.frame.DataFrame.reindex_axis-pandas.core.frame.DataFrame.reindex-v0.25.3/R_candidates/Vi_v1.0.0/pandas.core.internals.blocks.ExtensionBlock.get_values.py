    def get_values(self, dtype=None):
        # ExtensionArrays must be iterable, so this works.
        values = np.asarray(self.values)
        if values.ndim == self.ndim - 1:
            values = values.reshape((1,) + values.shape)
        return values
