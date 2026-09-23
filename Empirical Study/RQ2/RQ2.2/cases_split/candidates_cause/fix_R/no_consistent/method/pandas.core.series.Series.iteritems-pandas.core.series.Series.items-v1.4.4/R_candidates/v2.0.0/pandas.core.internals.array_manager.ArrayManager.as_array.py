    def as_array(
        self,
        dtype=None,
        copy: bool = False,
        na_value: object = lib.no_default,
    ) -> np.ndarray:
        """
        Convert the blockmanager data into an numpy array.

        Parameters
        ----------
        dtype : object, default None
            Data type of the return array.
        copy : bool, default False
            If True then guarantee that a copy is returned. A value of
            False does not guarantee that the underlying data is not
            copied.
        na_value : object, default lib.no_default
            Value to be used as the missing value sentinel.

        Returns
        -------
        arr : ndarray
        """
        if len(self.arrays) == 0:
            empty_arr = np.empty(self.shape, dtype=float)
            return empty_arr.transpose()

        # We want to copy when na_value is provided to avoid
        # mutating the original object
        copy = copy or na_value is not lib.no_default

        if not dtype:
            dtype = interleaved_dtype([arr.dtype for arr in self.arrays])

        if isinstance(dtype, SparseDtype):
            dtype = dtype.subtype
        elif isinstance(dtype, PandasDtype):
            dtype = dtype.numpy_dtype
        elif is_extension_array_dtype(dtype):
            dtype = "object"
        elif is_dtype_equal(dtype, str):
            dtype = "object"

        result = np.empty(self.shape_proper, dtype=dtype)

        for i, arr in enumerate(self.arrays):
            arr = arr.astype(dtype, copy=copy)
            result[:, i] = arr

        if na_value is not lib.no_default:
            result[isna(result)] = na_value

        return result
