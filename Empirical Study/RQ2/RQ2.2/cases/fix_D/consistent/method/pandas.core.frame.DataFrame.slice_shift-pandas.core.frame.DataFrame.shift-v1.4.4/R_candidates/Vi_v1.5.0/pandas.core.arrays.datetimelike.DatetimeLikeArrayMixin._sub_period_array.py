    @final
    def _sub_period_array(self, other: PeriodArray) -> npt.NDArray[np.object_]:
        if not is_period_dtype(self.dtype):
            raise TypeError(
                f"cannot subtract {other.dtype}-dtype from {type(self).__name__}"
            )

        self = cast("PeriodArray", self)
        self._require_matching_freq(other)

        new_i8_values = checked_add_with_arr(
            self.asi8, -other.asi8, arr_mask=self._isnan, b_mask=other._isnan
        )

        new_values = np.array([self.freq.base * x for x in new_i8_values])
        if self._hasna or other._hasna:
            mask = self._isnan | other._isnan
            new_values[mask] = NaT
        return new_values
