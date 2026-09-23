    def _validate(self):
        """Validate that we only store NA or strings."""
        if len(self._ndarray) and not lib.is_string_array(self._ndarray, skipna=True):
            raise ValueError("StringArray requires a sequence of strings or pandas.NA")
        if self._ndarray.dtype != "object":
            raise ValueError(
                "StringArray requires a sequence of strings or pandas.NA. Got "
                f"'{self._ndarray.dtype}' dtype instead."
            )
        # Check to see if need to convert Na values to pd.NA
        if self._ndarray.ndim > 2:
            # Ravel if ndims > 2 b/c no cythonized version available
            lib.convert_nans_to_NA(self._ndarray.ravel("K"))
        else:
            lib.convert_nans_to_NA(self._ndarray)
