    def _union(self, other, sort):
        if not len(other) or self.equals(other) or not len(self):
            return super()._union(other, sort=sort)

        # We are called by `union`, which is responsible for this validation
        assert isinstance(other, type(self))

        this, other = self._maybe_utc_convert(other)

        if this._can_fast_union(other):
            result = this._fast_union(other, sort=sort)
            if sort is None:
                # In the case where sort is None, _can_fast_union
                #  implies that result.freq should match self.freq
                assert result.freq == self.freq, (result.freq, self.freq)
            elif result.freq is None:
                # TODO: no tests rely on this; needed?
                result = result._with_freq("infer")
            return result
        else:
            i8self = Int64Index._simple_new(self.asi8)
            i8other = Int64Index._simple_new(other.asi8)
            i8result = i8self._union(i8other, sort=sort)
            # pandas\core\indexes\datetimelike.py:887: error: Unexpected
            # keyword argument "freq" for "DatetimeTimedeltaMixin"  [call-arg]
            result = type(self)(
                i8result, dtype=self.dtype, freq="infer"  # type: ignore[call-arg]
            )
            return result
