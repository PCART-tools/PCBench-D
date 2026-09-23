    @Appender((_round_doc + _ceil_example).format(op="ceil"))
    def ceil(
        self,
        freq,
        ambiguous: TimeAmbiguous = "raise",
        nonexistent: TimeNonexistent = "raise",
    ):
        return self._round(freq, RoundTo.PLUS_INFTY, ambiguous, nonexistent)
