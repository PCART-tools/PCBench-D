    def put(self, *args, **kwargs):
        """
        Applies the `put` method to its `values` attribute
        if it has one.

        See also
        --------
        numpy.ndarray.put
        """
        self._values.put(*args, **kwargs)
