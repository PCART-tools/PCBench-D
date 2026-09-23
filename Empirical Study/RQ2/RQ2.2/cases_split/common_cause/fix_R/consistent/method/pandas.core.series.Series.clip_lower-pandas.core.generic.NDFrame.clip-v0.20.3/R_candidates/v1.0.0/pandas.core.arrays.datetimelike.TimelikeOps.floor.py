    @Appender((_round_doc + _floor_example).format(op="floor"))
    def floor(self, freq, ambiguous="raise", nonexistent="raise"):
        return self._round(freq, RoundTo.MINUS_INFTY, ambiguous, nonexistent)
