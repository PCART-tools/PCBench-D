    def repeat(self, repeats, *args, **kwargs):
        """
        Repeat elements of an array.

        See Also
        --------
        numpy.ndarray.repeat
        """
        nv.validate_repeat(args, kwargs)
        values = self._data.repeat(repeats)
        return type(self)(values.view('i8'), dtype=self.dtype)
