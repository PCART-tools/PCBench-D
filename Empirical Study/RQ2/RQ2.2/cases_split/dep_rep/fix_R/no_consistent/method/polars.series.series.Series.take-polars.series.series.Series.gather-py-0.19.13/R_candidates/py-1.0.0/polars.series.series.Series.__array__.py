    def __array__(
        self, dtype: npt.DTypeLike | None = None, copy: bool | None = None
    ) -> np.ndarray[Any, Any]:
        """
        Return a NumPy ndarray with the given data type.

        This method ensures a Polars Series can be treated as a NumPy ndarray.
        It enables `np.asarray` and NumPy universal functions.

        See the NumPy documentation for more information:
        https://numpy.org/doc/stable/user/basics.interoperability.html#the-array-method

        See Also
        --------
        __array_ufunc__
        """
        # Cast String types to fixed-length string to support string ufuncs
        # TODO: Use variable-length strings instead when NumPy 2.0.0 comes out:
        # https://numpy.org/devdocs/reference/routines.dtypes.html#numpy.dtypes.StringDType
        if dtype is None and not self.has_nulls() and self.dtype == String:
            dtype = np.dtype("U")

        if copy is None:
            writable, allow_copy = False, True
        elif copy is True:
            writable, allow_copy = True, True
        elif copy is False:
            writable, allow_copy = False, False
        else:
            msg = f"invalid input for `copy`: {copy!r}"
            raise TypeError(msg)

        arr = self.to_numpy(writable=writable, allow_copy=allow_copy)

        if dtype is not None and dtype != arr.dtype:
            if copy is False:
                # TODO: Only raise when data must be copied
                msg = f"copy not allowed: cast from {arr.dtype} to {dtype} prohibited"
                raise RuntimeError(msg)

            arr = arr.__array__(dtype)

        return arr
