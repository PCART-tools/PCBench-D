    @Appender((_round_doc + _round_example).format(op="round"))
    def round(
        self,
        freq,
        ambiguous: TimeAmbiguous = "raise",
        nonexistent: TimeNonexistent = "raise",
    ) -> Self:
        return self._round(freq, RoundTo.NEAREST_HALF_EVEN, ambiguous, nonexistent)
