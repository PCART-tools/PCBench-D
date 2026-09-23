    def make_empty(self, axes=None) -> Self:
        """Return an empty ArrayManager with the items axis of len 0 (no columns)"""
        if axes is None:
            axes = [self.axes[1:], Index([])]

        arrays: list[np.ndarray | ExtensionArray] = []
        return type(self)(arrays, axes)
