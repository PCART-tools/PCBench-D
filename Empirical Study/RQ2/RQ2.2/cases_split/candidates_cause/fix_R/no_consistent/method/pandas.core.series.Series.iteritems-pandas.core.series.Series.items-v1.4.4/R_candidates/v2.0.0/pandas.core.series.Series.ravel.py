    def ravel(self, order: str = "C") -> ArrayLike:
        """
        Return the flattened underlying data as an ndarray or ExtensionArray.

        Returns
        -------
        numpy.ndarray or ExtensionArray
            Flattened data of the Series.

        See Also
        --------
        numpy.ndarray.ravel : Return a flattened array.
        """
        arr = self._values.ravel(order=order)
        if isinstance(arr, np.ndarray) and using_copy_on_write():
            arr.flags.writeable = False
        return arr
