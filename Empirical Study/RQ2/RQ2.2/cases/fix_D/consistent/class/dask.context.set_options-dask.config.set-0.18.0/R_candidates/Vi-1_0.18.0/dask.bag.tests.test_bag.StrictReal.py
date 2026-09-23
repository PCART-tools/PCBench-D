class StrictReal(int):
    def __eq__(self, other):
        assert isinstance(other, StrictReal)
        return self.real == other.real

    def __ne__(self, other):
        assert isinstance(other, StrictReal)
        return self.real != other.real
