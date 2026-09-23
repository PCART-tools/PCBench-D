    def __eq__(self, other):
        if not isinstance(other, MultivarColormap):
            return False
        if len(self) != len(other):
            return False
        for c0, c1 in zip(self, other):
            if c0 != c1:
                return False
        if not all(self._rgba_bad == other._rgba_bad):
            return False
        if self.combination_mode != other.combination_mode:
            return False
        return True
