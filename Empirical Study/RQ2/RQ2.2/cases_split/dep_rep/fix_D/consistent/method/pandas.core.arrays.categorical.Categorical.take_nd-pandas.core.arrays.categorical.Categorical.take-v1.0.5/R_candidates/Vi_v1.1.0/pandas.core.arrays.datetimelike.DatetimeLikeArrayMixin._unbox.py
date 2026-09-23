    def _unbox(self, other) -> Union[np.int64, np.ndarray]:
        """
        Unbox either a scalar with _unbox_scalar or an instance of our own type.
        """
        if lib.is_scalar(other):
            other = self._unbox_scalar(other)
        else:
            # same type as self
            self._check_compatible_with(other)
            other = other.view("i8")
        return other
