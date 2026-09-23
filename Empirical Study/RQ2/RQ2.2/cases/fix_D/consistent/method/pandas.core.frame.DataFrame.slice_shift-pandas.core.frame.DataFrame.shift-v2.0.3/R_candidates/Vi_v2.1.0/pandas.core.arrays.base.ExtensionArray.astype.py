    def astype(self, dtype: AstypeArg, copy: bool = True) -> ArrayLike:
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
        np.ndarray or pandas.api.extensions.ExtensionArray
            An ``ExtensionArray`` if ``dtype`` is ``ExtensionDtype``,
            otherwise a Numpy ndarray with ``dtype`` for its dtype.

        Examples
        --------
        >>> arr = pd.array([1, 2, 3])
        >>> arr
        <IntegerArray>
        [1, 2, 3]
        Length: 3, dtype: Int64

        Casting to another ``ExtensionDtype`` returns an ``ExtensionArray``:

        >>> arr1 = arr.astype('Float64')
        >>> arr1
        <FloatingArray>
        [1.0, 2.0, 3.0]
        Length: 3, dtype: Float64
        >>> arr1.dtype
        Float64Dtype()

        Otherwise, we will get a Numpy ndarray:

        >>> arr2 = arr.astype('float64')
        >>> arr2
        array([1., 2., 3.])
        >>> arr2.dtype
        dtype('float64')
        """
        dtype = pandas_dtype(dtype)
        if dtype == self.dtype:
            if not copy:
                return self
            else:
                return self.copy()

        if isinstance(dtype, ExtensionDtype):
            cls = dtype.construct_array_type()
            return cls._from_sequence(self, dtype=dtype, copy=copy)

        elif lib.is_np_dtype(dtype, "M"):
            from pandas.core.arrays import DatetimeArray

            return DatetimeArray._from_sequence(self, dtype=dtype, copy=copy)

        elif lib.is_np_dtype(dtype, "m"):
            from pandas.core.arrays import TimedeltaArray

            return TimedeltaArray._from_sequence(self, dtype=dtype, copy=copy)

        return np.array(self, dtype=dtype, copy=copy)
