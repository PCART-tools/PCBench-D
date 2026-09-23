    @final
    def _sub_period(self, other: Period) -> npt.NDArray[np.object_]:
        if not is_period_dtype(self.dtype):
            raise TypeError(f"cannot subtract Period from a {type(self).__name__}")

        # If the operation is well-defined, we return an object-dtype ndarray
        # of DateOffsets.  Null entries are filled with pd.NaT
        self._check_compatible_with(other)
        new_i8_data = checked_add_with_arr(
            self.asi8, -other.ordinal, arr_mask=self._isnan
        )
        new_data = np.array([self.freq.base * x for x in new_i8_data])

        if self._hasna:
            new_data[self._isnan] = NaT

        return new_data
