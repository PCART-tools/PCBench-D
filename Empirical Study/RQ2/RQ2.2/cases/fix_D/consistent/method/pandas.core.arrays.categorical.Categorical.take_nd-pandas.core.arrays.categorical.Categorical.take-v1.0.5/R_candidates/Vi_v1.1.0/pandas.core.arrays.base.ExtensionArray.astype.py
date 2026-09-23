    def astype(self, dtype, copy=True):
        """
        Cast to a NumPy array with 'dtype'.

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
        array : ndarray
            NumPy ndarray with 'dtype' for its dtype.
        """
        from pandas.core.arrays.string_ import StringDtype

        dtype = pandas_dtype(dtype)
        if isinstance(dtype, StringDtype):  # allow conversion to StringArrays
            return dtype.construct_array_type()._from_sequence(self, copy=False)

        return np.array(self, dtype=dtype, copy=copy)
