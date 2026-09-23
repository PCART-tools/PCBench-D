    def _can_range_setop(self, other):
        return isinstance(self.freq, Tick) and isinstance(other.freq, Tick)
