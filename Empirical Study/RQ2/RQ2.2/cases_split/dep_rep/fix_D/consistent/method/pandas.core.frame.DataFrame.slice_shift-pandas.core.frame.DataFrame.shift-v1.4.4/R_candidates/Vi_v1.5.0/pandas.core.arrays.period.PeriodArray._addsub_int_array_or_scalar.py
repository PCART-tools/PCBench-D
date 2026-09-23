    def _addsub_int_array_or_scalar(
        self, other: np.ndarray | int, op: Callable[[Any, Any], Any]
    ) -> PeriodArray:
        """
        Add or subtract array of integers; equivalent to applying
        `_time_shift` pointwise.

        Parameters
        ----------
        other : np.ndarray[int64] or int
        op : {operator.add, operator.sub}

        Returns
        -------
        result : PeriodArray
        """
        assert op in [operator.add, operator.sub]
        if op is operator.sub:
            other = -other
        res_values = algos.checked_add_with_arr(self.asi8, other, arr_mask=self._isnan)
        return type(self)(res_values, freq=self.freq)
