    def _add_offset(self, other: BaseOffset):
        assert not isinstance(other, Tick)

        self._require_matching_freq(other, base=True)

        # Note: when calling parent class's _add_timedeltalike_scalar,
        #  it will call delta_to_nanoseconds(delta).  Because delta here
        #  is an integer, delta_to_nanoseconds will return it unchanged.
        result = super()._add_timedeltalike_scalar(other.n)
        return type(self)(result, freq=self.freq)
