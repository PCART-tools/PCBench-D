    def _add_offset(self, other: BaseOffset):
        assert not isinstance(other, Tick)

        self._require_matching_freq(other, base=True)
        return self._addsub_int_array_or_scalar(other.n, operator.add)
