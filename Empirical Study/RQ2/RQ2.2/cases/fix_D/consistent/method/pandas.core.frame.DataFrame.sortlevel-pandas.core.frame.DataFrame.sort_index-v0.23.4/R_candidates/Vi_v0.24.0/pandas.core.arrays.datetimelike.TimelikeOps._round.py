    def _round(self, freq, mode, ambiguous, nonexistent):
        # round the local times
        values = _ensure_datetimelike_to_i8(self)
        result = round_nsint64(values, mode, freq)
        result = self._maybe_mask_results(result, fill_value=NaT)

        dtype = self.dtype
        if is_datetime64tz_dtype(self):
            dtype = None
        return self._ensure_localized(
            self._simple_new(result, dtype=dtype), ambiguous, nonexistent
        )
