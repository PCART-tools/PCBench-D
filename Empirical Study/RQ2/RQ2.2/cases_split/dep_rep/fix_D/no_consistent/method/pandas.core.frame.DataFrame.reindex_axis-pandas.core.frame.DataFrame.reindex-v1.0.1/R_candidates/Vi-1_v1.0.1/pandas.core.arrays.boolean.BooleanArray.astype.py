    def astype(self, dtype, copy=True):
        """
        Cast to a NumPy array or ExtensionArray with 'dtype'.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        copy : bool, default True
            Whether to copy the data, even if not necessary. If False,
            a copy is made only if the old dtype does not match the
            new dtype.

        Returns
        -------
        array : ndarray or ExtensionArray
            NumPy ndarray, BooleanArray or IntergerArray with 'dtype' for its dtype.

        Raises
        ------
        TypeError
            if incompatible type with an BooleanDtype, equivalent of same_kind
            casting
        """
        dtype = pandas_dtype(dtype)

        if isinstance(dtype, BooleanDtype):
            values, mask = coerce_to_array(self, copy=copy)
            return BooleanArray(values, mask, copy=False)

        if is_bool_dtype(dtype):
            # astype_nansafe converts np.nan to True
            if self._hasna:
                raise ValueError("cannot convert float NaN to bool")
            else:
                return self._data.astype(dtype, copy=copy)
        if is_extension_array_dtype(dtype) and is_integer_dtype(dtype):
            from pandas.core.arrays import IntegerArray

            return IntegerArray(
                self._data.astype(dtype.numpy_dtype), self._mask.copy(), copy=False
            )
        # for integer, error if there are missing values
        if is_integer_dtype(dtype):
            if self._hasna:
                raise ValueError("cannot convert NA to integer")
        # for float dtype, ensure we use np.nan before casting (numpy cannot
        # deal with pd.NA)
        na_value = self._na_value
        if is_float_dtype(dtype):
            na_value = np.nan
        # coerce
        data = self.to_numpy(na_value=na_value)
        return astype_nansafe(data, dtype, copy=False)
