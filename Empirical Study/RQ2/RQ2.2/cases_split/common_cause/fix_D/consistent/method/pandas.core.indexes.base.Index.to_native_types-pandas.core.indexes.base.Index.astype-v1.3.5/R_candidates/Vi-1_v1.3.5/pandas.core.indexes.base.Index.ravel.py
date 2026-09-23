    @final
    def ravel(self, order="C"):
        """
        Return an ndarray of the flattened values of the underlying data.

        Returns
        -------
        numpy.ndarray
            Flattened array.

        See Also
        --------
        numpy.ndarray.ravel : Return a flattened array.
        """
        warnings.warn(
            "Index.ravel returning ndarray is deprecated; in a future version "
            "this will return a view on self.",
            FutureWarning,
            stacklevel=2,
        )
        values = self._get_engine_target()
        return values.ravel(order=order)
