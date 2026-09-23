    def equals(self, other):
        """Returns True if self and other are the same mathematical entities"""
        return isinstance(other, self.func) and list(
            ordered(self.args)) == list(ordered(other.args))
