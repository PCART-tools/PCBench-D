    def _check_compatible_with(self, other, setitem: bool = False):
        if other is NaT:
            return
        if self.freqstr != other.freqstr:
            raise raise_on_incompatible(self, other)
