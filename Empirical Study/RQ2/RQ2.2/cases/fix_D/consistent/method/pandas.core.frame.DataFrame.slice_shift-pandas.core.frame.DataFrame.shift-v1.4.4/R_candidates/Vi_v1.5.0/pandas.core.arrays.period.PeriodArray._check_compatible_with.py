    def _check_compatible_with(self, other, setitem: bool = False):
        if other is NaT:
            return
        self._require_matching_freq(other)
