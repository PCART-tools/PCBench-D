    def astype(self, dtype, copy: bool = True) -> ArrayLike:
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
        ndarray or ExtensionArray
            NumPy ndarray, BooleanArray or IntegerArray with 'dtype' for its dtype.

        Raises
        ------
        TypeError
            if incompatible type with an IntegerDtype, equivalent of same_kind
            casting
        """
        from pandas.core.arrays.masked import BaseMaskedDtype
        from pandas.core.arrays.string_ import StringDtype

        dtype = pandas_dtype(dtype)

        # if the dtype is exactly the same, we can fastpath
        if self.dtype == dtype:
            # return the same object for copy=False
            return self.copy() if copy else self
        # if we are astyping to another nullable masked dtype, we can fastpath
        if isinstance(dtype, BaseMaskedDtype):
            data = self._data.astype(dtype.numpy_dtype, copy=copy)
            # mask is copied depending on whether the data was copied, and
            # not directly depending on the `copy` keyword
            mask = self._mask if data is self._data else self._mask.copy()
            return dtype.construct_array_type()(data, mask, copy=False)
        elif isinstance(dtype, StringDtype):
            return dtype.construct_array_type()._from_sequence(self, copy=False)

        # coerce
        if is_float_dtype(dtype):
            # In astype, we consider dtype=float to also mean na_value=np.nan
            na_value = np.nan
        elif is_datetime64_dtype(dtype):
            na_value = np.datetime64("NaT")
        else:
            na_value = lib.no_default

        return self.to_numpy(dtype=dtype, na_value=na_value, copy=False)
