    def _union(self, other, sort):
        if not len(other) or self.equals(other) or not len(self):
            return super()._union(other, sort=sort)

        if len(other) == 0 or self.equals(other) or len(self) == 0:
            return super().union(other, sort=sort)

        if not isinstance(other, DatetimeIndex):
            try:
                other = DatetimeIndex(other)
            except TypeError:
                pass

        this, other = self._maybe_utc_convert(other)

        if this._can_fast_union(other):
            return this._fast_union(other, sort=sort)
        else:
            result = Index._union(this, other, sort=sort)
            if isinstance(result, DatetimeIndex):
                # TODO: we shouldn't be setting attributes like this;
                #  in all the tests this equality already holds
                result._data._dtype = this.dtype
                if result.freq is None and (
                    this.freq is not None or other.freq is not None
                ):
                    result.freq = to_offset(result.inferred_freq)
            return result
