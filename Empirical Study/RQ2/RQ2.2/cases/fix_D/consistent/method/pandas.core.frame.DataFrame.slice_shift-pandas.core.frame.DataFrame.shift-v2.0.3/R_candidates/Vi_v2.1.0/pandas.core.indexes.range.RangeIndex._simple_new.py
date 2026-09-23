    @classmethod
    def _simple_new(  # type: ignore[override]
        cls, values: range, name: Hashable | None = None
    ) -> Self:
        result = object.__new__(cls)

        assert isinstance(values, range)

        result._range = values
        result._name = name
        result._cache = {}
        result._reset_identity()
        result._references = None
        return result
