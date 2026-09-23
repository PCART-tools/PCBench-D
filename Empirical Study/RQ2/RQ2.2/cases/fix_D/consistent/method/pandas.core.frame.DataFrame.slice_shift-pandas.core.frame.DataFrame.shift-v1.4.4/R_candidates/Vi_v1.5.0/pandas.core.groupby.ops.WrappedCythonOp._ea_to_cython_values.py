    def _ea_to_cython_values(self, values: ExtensionArray) -> np.ndarray:
        # GH#43682
        if isinstance(values, (DatetimeArray, PeriodArray, TimedeltaArray)):
            # All of the functions implemented here are ordinal, so we can
            #  operate on the tz-naive equivalents
            npvalues = values._ndarray.view("M8[ns]")
        elif isinstance(values.dtype, (BooleanDtype, IntegerDtype)):
            # IntegerArray or BooleanArray
            npvalues = values.to_numpy("float64", na_value=np.nan)
        elif isinstance(values.dtype, FloatingDtype):
            # FloatingArray
            npvalues = values.to_numpy(values.dtype.numpy_dtype, na_value=np.nan)
        elif isinstance(values.dtype, StringDtype):
            # StringArray
            npvalues = values.to_numpy(object, na_value=np.nan)
        else:
            raise NotImplementedError(
                f"function is not implemented for this dtype: {values.dtype}"
            )
        return npvalues
