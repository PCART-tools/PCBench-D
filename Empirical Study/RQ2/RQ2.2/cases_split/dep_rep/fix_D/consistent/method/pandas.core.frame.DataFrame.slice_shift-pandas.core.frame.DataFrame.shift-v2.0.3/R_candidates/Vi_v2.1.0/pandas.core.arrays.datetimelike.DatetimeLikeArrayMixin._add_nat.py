    @final
    def _add_nat(self):
        """
        Add pd.NaT to self
        """
        if isinstance(self.dtype, PeriodDtype):
            raise TypeError(
                f"Cannot add {type(self).__name__} and {type(NaT).__name__}"
            )
        self = cast("TimedeltaArray | DatetimeArray", self)

        # GH#19124 pd.NaT is treated like a timedelta for both timedelta
        # and datetime dtypes
        result = np.empty(self.shape, dtype=np.int64)
        result.fill(iNaT)
        result = result.view(self._ndarray.dtype)  # preserve reso
        # error: Argument "dtype" to "_simple_new" of "DatetimeArray" has
        # incompatible type "Union[dtype[timedelta64], dtype[datetime64],
        # DatetimeTZDtype]"; expected "Union[dtype[datetime64], DatetimeTZDtype]"
        return type(self)._simple_new(
            result, dtype=self.dtype, freq=None  # type: ignore[arg-type]
        )
