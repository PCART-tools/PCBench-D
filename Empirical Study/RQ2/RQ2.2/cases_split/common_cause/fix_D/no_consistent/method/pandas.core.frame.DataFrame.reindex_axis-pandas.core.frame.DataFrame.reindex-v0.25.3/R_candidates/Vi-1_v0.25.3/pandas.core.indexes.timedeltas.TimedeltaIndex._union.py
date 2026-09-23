    def _union(self, other, sort):
        if len(other) == 0 or self.equals(other) or len(self) == 0:
            return super()._union(other, sort=sort)

        if not isinstance(other, TimedeltaIndex):
            try:
                other = TimedeltaIndex(other)
            except (TypeError, ValueError):
                pass
        this, other = self, other

        if this._can_fast_union(other):
            return this._fast_union(other)
        else:
            result = Index._union(this, other, sort=sort)
            if isinstance(result, TimedeltaIndex):
                if result.freq is None:
                    result.freq = to_offset(result.inferred_freq)
            return result
