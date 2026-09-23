    def _can_fast_intersect(self: _T, other: _T) -> bool:
        if self.freq is None:
            return False

        elif other.freq != self.freq:
            return False

        elif not self.is_monotonic_increasing:
            # Because freq is not None, we must then be monotonic decreasing
            return False

        elif self.freq.is_anchored():
            # this along with matching freqs ensure that we "line up",
            #  so intersection will preserve freq
            return True

        elif isinstance(self.freq, Tick):
            # We "line up" if and only if the difference between two of our points
            #  is a multiple of our freq
            diff = self[0] - other[0]
            remainder = diff % self.freq.delta
            return remainder == Timedelta(0)

        return True
