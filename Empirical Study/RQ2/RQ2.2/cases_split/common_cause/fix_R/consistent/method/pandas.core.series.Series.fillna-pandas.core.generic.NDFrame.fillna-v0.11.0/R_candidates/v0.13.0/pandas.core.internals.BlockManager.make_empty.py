    def make_empty(self, axes=None):
        """ return an empty BlockManager with the items axis of len 0 """
        if axes is None:
            axes = [_ensure_index([])] + [
                _ensure_index(a) for a in self.axes[1:]
            ]

        # preserve dtype if possible
        dtype = self.dtype if self.ndim == 1 else object
        return self.__class__(np.array([], dtype=dtype), axes)
