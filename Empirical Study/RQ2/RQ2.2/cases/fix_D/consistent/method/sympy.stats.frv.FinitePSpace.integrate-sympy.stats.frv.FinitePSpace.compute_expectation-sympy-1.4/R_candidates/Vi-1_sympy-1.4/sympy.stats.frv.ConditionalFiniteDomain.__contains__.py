    def __contains__(self, other):
        return other in self.fulldomain and self._test(other)
