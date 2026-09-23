    def _from_combined(self, combined: np.ndarray) -> IntervalArray:
        """
        Create a new IntervalArray with our dtype from a 1D complex128 ndarray.
        """
        nc = combined.view("i8").reshape(-1, 2)

        dtype = self._left.dtype
        if needs_i8_conversion(dtype):
            new_left = type(self._left)._from_sequence(nc[:, 0], dtype=dtype)
            new_right = type(self._right)._from_sequence(nc[:, 1], dtype=dtype)
        else:
            new_left = nc[:, 0].view(dtype)
            new_right = nc[:, 1].view(dtype)
        return self._shallow_copy(left=new_left, right=new_right)
