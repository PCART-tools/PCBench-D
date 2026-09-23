    def _dt_ceil(
        self,
        freq,
        ambiguous: TimeAmbiguous = "raise",
        nonexistent: TimeNonexistent = "raise",
    ):
        return self._round_temporally("ceil", freq, ambiguous, nonexistent)
