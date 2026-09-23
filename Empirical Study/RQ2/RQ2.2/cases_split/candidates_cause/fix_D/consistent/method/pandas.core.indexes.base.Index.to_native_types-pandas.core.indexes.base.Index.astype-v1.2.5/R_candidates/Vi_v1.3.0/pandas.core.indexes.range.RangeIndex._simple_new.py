    @classmethod
    def _simple_new(cls, values: range, name: Hashable = None) -> RangeIndex:
        result = object.__new__(cls)

        assert isinstance(values, range)

        result._range = values
        result._name = name
        result._cache = {}
        result._reset_identity()
        return result
