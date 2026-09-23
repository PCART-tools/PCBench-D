    @classmethod
    def _simple_new(
        cls,
        values: Union[DatetimeArray, TimedeltaArray, PeriodArray],
        name: Label = None,
    ):
        assert isinstance(values, cls._data_cls), type(values)

        result = object.__new__(cls)
        result._data = values
        result._name = name
        result._cache = {}

        # For groupby perf. See note in indexes/base about _index_data
        result._index_data = values._data

        result._reset_identity()
        return result
