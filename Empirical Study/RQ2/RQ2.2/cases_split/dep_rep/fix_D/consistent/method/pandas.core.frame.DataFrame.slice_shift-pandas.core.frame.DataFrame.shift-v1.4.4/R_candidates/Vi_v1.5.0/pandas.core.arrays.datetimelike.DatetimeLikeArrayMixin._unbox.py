    def _unbox(
        self, other, setitem: bool = False
    ) -> np.int64 | np.datetime64 | np.timedelta64 | np.ndarray:
        """
        Unbox either a scalar with _unbox_scalar or an instance of our own type.
        """
        if lib.is_scalar(other):
            other = self._unbox_scalar(other, setitem=setitem)
        else:
            # same type as self
            self._check_compatible_with(other, setitem=setitem)
            other = other._ndarray
        return other
