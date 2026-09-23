    def _union(self, other, sort):
        if not len(other) or self.equals(other) or not len(self):
            return super()._union(other, sort=sort)

        # We are called by `union`, which is responsible for this validation
        assert isinstance(other, type(self))

        this, other = self._maybe_utc_convert(other)

        if this._can_fast_union(other):
            return this._fast_union(other, sort=sort)
        else:
            result = Index._union(this, other, sort=sort)
            if isinstance(result, type(self)):
                assert result._data.dtype == this.dtype
                if result.freq is None:
                    result._set_freq("infer")
            return result
