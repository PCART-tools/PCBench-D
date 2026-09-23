    def identical(self, other):
        """Similar to equals, but check that other comparable attributes are
        also equal
        """
        return (self.equals(other) and
                all((getattr(self, c, None) == getattr(other, c, None)
                     for c in self._comparables)))
