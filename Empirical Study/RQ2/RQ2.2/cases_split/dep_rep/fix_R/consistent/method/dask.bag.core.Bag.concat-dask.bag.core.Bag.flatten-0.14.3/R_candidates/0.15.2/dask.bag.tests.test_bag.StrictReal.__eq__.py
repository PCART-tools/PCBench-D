    def __eq__(self, other):
        assert isinstance(other, StrictReal)
        return self.real == other.real
