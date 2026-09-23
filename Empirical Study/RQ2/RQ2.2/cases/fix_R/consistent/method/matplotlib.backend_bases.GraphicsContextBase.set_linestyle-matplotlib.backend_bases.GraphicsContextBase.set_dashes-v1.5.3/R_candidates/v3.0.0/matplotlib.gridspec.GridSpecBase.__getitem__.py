    def __getitem__(self, key):
        """Create and return a SuplotSpec instance.
        """
        nrows, ncols = self.get_geometry()

        def _normalize(key, size):  # Includes last index.
            if isinstance(key, slice):
                start, stop, _ = key.indices(size)
                if stop > start:
                    return start, stop - 1
            else:
                if key < 0:
                    key += size
                if 0 <= key < size:
                    return key, key
            raise IndexError("invalid index")

        if isinstance(key, tuple):
            try:
                k1, k2 = key
            except ValueError:
                raise ValueError("unrecognized subplot spec")
            num1, num2 = np.ravel_multi_index(
                [_normalize(k1, nrows), _normalize(k2, ncols)], (nrows, ncols))
        else:  # Single key
            num1, num2 = _normalize(key, nrows * ncols)

        return SubplotSpec(self, num1, num2)
