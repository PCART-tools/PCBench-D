    def repeat(self: _T, repeats, axis=None) -> _T:
        """
        Repeat elements of an array.

        See Also
        --------
        numpy.ndarray.repeat
        """
        nv.validate_repeat(tuple(), dict(axis=axis))
        new_data = self._ndarray.repeat(repeats, axis=axis)
        return self._from_backing_data(new_data)
