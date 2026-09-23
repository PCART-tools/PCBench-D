    def __eq__(self, other):
        return isinstance(other, _StrongRef) and self._obj == other._obj
