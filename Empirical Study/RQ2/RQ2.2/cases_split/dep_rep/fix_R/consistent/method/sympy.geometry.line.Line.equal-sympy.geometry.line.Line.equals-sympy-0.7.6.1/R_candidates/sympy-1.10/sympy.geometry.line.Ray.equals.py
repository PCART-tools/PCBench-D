    def equals(self, other):
        """Returns True if self and other are the same mathematical entities"""
        if not isinstance(other, Ray):
            return False
        return self.source == other.source and other.p2 in self
