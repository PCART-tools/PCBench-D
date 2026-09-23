    def _wrap_ndarray_result(self, result: np.ndarray):
        # If we have timedelta64[ns] result, return a TimedeltaArray instead
        #  of a PandasArray
        if result.dtype == "timedelta64[ns]":
            from pandas.core.arrays import TimedeltaArray

            return TimedeltaArray._simple_new(result)
        return type(self)(result)
