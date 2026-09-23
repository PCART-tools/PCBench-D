    def _check_compatible_with(self, other):
        if other is NaT:
            return
        if self.freqstr != other.freqstr:
            _raise_on_incompatible(self, other)
