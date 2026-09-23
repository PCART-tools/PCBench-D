    def _wrap_ndarray_result(self, result: np.ndarray):
        # If we have timedelta64[ns] result, return a TimedeltaArray instead
        #  of a NumpyExtensionArray
        if result.dtype.kind == "m" and is_supported_unit(
            get_unit_from_dtype(result.dtype)
        ):
            from pandas.core.arrays import TimedeltaArray

            return TimedeltaArray._simple_new(result, dtype=result.dtype)
        return type(self)(result)
