    def _round(self, freq, mode, ambiguous, nonexistent):
        # round the local times
        if is_datetime64tz_dtype(self.dtype):
            # operate on naive timestamps, then convert back to aware
            self = cast("DatetimeArray", self)
            naive = self.tz_localize(None)
            result = naive._round(freq, mode, ambiguous, nonexistent)
            return result.tz_localize(
                self.tz, ambiguous=ambiguous, nonexistent=nonexistent
            )

        values = self.view("i8")
        values = cast(np.ndarray, values)
        nanos = to_offset(freq).nanos  # raises on non-fixed frequencies
        nanos = delta_to_nanoseconds(to_offset(freq), self._creso)
        result_i8 = round_nsint64(values, mode, nanos)
        result = self._maybe_mask_results(result_i8, fill_value=iNaT)
        result = result.view(self._ndarray.dtype)
        return self._simple_new(result, dtype=self.dtype)
