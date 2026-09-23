    def _add_timedelta_arraylike(
        self, other: TimedeltaArray | npt.NDArray[np.timedelta64]
    ) -> PeriodArray:
        """
        Parameters
        ----------
        other : TimedeltaArray or ndarray[timedelta64]

        Returns
        -------
        PeriodArray
        """
        freq = self.freq
        if not isinstance(freq, Tick):
            # We cannot add timedelta-like to non-tick PeriodArray
            raise TypeError(
                f"Cannot add or subtract timedelta64[ns] dtype from {self.dtype}"
            )

        dtype = np.dtype(f"m8[{freq._td64_unit}]")

        try:
            delta = astype_overflowsafe(
                np.asarray(other), dtype=dtype, copy=False, round_ok=False
            )
        except ValueError as err:
            # e.g. if we have minutes freq and try to add 30s
            # "Cannot losslessly convert units"
            raise IncompatibleFrequency(
                "Cannot add/subtract timedelta-like from PeriodArray that is "
                "not an integer multiple of the PeriodArray's freq."
            ) from err

        b_mask = np.isnat(delta)

        res_values = algos.checked_add_with_arr(
            self.asi8, delta.view("i8"), arr_mask=self._isnan, b_mask=b_mask
        )
        np.putmask(res_values, self._isnan | b_mask, iNaT)
        return type(self)(res_values, freq=self.freq)
