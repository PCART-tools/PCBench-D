    def _round(self, freq, mode, ambiguous, nonexistent):
        # round the local times
        if is_datetime64tz_dtype(self.dtype):
            # operate on naive timestamps, then convert back to aware
            naive = self.tz_localize(None)
            result = naive._round(freq, mode, ambiguous, nonexistent)
            aware = result.tz_localize(
                self.tz, ambiguous=ambiguous, nonexistent=nonexistent
            )
            return aware

        values = self.view("i8")
        result = round_nsint64(values, mode, freq)
        result = self._maybe_mask_results(result, fill_value=NaT)
        return self._simple_new(result, dtype=self.dtype)
