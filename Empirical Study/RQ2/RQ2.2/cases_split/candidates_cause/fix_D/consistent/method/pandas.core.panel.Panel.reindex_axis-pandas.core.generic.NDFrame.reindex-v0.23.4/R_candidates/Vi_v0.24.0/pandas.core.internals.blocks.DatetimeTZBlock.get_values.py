    def get_values(self, dtype=None):
        """
        Returns an ndarray of values.

        Parameters
        ----------
        dtype : np.dtype
            Only `object`-like dtypes are respected here (not sure
            why).

        Returns
        -------
        values : ndarray
            When ``dtype=object``, then and object-dtype ndarray of
            boxed values is returned. Otherwise, an M8[ns] ndarray
            is returned.

            DatetimeArray is always 1-d. ``get_values`` will reshape
            the return value to be the same dimensionality as the
            block.
        """
        values = self.values
        if is_object_dtype(dtype):
            values = values._box_values(values._data)

        values = np.asarray(values)

        if self.ndim == 2:
            # Ensure that our shape is correct for DataFrame.
            # ExtensionArrays are always 1-D, even in a DataFrame when
            # the analogous NumPy-backed column would be a 2-D ndarray.
            values = values.reshape(1, -1)
        return values
