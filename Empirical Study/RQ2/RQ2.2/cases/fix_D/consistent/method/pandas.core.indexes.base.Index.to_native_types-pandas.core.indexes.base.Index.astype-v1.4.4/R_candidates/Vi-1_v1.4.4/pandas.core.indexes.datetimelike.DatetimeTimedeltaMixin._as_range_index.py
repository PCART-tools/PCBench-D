    @cache_readonly
    def _as_range_index(self) -> RangeIndex:
        # Convert our i8 representations to RangeIndex
        # Caller is responsible for checking isinstance(self.freq, Tick)
        freq = cast(Tick, self.freq)
        tick = freq.delta.value
        rng = range(self[0].value, self[-1].value + tick, tick)
        return RangeIndex(rng)
