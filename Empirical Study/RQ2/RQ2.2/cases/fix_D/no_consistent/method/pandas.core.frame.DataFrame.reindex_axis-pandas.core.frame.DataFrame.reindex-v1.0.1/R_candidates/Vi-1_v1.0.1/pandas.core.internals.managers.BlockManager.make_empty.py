    def make_empty(self, axes=None):
        """ return an empty BlockManager with the items axis of len 0 """
        if axes is None:
            axes = [ensure_index([])] + [ensure_index(a) for a in self.axes[1:]]

        # preserve dtype if possible
        if self.ndim == 1:
            blocks = np.array([], dtype=self.array_dtype)
        else:
            blocks = []
        return type(self)(blocks, axes)
