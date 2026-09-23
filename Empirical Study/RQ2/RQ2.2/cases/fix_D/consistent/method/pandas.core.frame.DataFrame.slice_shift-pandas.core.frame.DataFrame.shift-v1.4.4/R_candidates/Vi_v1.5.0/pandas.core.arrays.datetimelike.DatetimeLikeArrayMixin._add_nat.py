    @final
    def _add_nat(self):
        """
        Add pd.NaT to self
        """
        if is_period_dtype(self.dtype):
            raise TypeError(
                f"Cannot add {type(self).__name__} and {type(NaT).__name__}"
            )
        self = cast("TimedeltaArray | DatetimeArray", self)

        # GH#19124 pd.NaT is treated like a timedelta for both timedelta
        # and datetime dtypes
        result = np.empty(self.shape, dtype=np.int64)
        result.fill(iNaT)
        result = result.view(self._ndarray.dtype)  # preserve reso
        return type(self)._simple_new(result, dtype=self.dtype, freq=None)
