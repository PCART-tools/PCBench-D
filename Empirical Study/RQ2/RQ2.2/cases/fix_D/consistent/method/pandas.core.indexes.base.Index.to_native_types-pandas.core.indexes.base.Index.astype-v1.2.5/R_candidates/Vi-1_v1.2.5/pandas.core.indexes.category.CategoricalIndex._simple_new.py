    @classmethod
    def _simple_new(cls, values: Categorical, name: Label = None):
        assert isinstance(values, Categorical), type(values)
        result = object.__new__(cls)

        result._data = values
        result.name = name
        result._cache = {}

        result._reset_identity()
        return result
