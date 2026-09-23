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
            stacklevel=find_stack_level(),
        )
        if needs_i8_conversion(self.dtype):
            # Item "ndarray[Any, Any]" of "Union[ExtensionArray, ndarray[Any, Any]]"
            # has no attribute "_ndarray"
            values = self._data._ndarray  # type: ignore[union-attr]
        elif is_interval_dtype(self.dtype):
            values = np.asarray(self._data)
        else:
            values = self._get_engine_target()
        return values.ravel(order=order)
