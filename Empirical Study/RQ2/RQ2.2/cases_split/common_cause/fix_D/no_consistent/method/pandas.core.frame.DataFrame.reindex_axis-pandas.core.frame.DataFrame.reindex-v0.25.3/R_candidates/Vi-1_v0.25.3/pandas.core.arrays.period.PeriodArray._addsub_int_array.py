    @Appender(dtl.DatetimeLikeArrayMixin._addsub_int_array.__doc__)
    def _addsub_int_array(
        self,
        other: Union[ABCPeriodArray, ABCSeries, ABCPeriodIndex, np.ndarray],
        op: Callable[[Any], Any],
    ) -> ABCPeriodArray:
        assert op in [operator.add, operator.sub]
        if op is operator.sub:
            other = -other
        res_values = algos.checked_add_with_arr(self.asi8, other, arr_mask=self._isnan)
        res_values = res_values.view("i8")
        res_values[self._isnan] = iNaT
        return type(self)(res_values, freq=self.freq)
