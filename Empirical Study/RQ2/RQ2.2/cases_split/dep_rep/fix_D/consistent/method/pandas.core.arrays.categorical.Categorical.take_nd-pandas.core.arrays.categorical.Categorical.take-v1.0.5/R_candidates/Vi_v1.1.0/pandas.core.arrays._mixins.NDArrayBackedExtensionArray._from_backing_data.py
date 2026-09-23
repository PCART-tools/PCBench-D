    def _from_backing_data(self: _T, arr: np.ndarray) -> _T:
        """
        Construct a new ExtensionArray `new_array` with `arr` as its _ndarray.

        This should round-trip:
            self == self._from_backing_data(self._ndarray)
        """
        raise AbstractMethodError(self)
