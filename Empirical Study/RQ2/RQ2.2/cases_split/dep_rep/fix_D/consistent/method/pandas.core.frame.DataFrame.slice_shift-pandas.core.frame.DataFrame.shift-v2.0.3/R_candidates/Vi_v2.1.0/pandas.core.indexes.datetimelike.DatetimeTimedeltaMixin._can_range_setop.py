    def _can_range_setop(self, other) -> bool:
        return isinstance(self.freq, Tick) and isinstance(other.freq, Tick)
