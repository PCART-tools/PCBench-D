    def _add_timedeltalike_scalar(self, other):
        """
        Add a delta of a timedeltalike
        return the i8 result view
        """
        if isna(other):
            # i.e np.timedelta64("NaT"), not recognized by delta_to_nanoseconds
            new_values = np.empty(len(self), dtype="i8")
            new_values[:] = iNaT
            return new_values

        inc = delta_to_nanoseconds(other)
        new_values = checked_add_with_arr(self.asi8, inc, arr_mask=self._isnan).view(
            "i8"
        )
        new_values = self._maybe_mask_results(new_values)
        return new_values.view("i8")
