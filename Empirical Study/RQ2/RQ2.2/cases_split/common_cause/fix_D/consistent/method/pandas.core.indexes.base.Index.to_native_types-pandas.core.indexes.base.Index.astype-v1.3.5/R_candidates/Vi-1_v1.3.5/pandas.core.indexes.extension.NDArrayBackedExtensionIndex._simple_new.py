    @classmethod
    def _simple_new(
        cls,
        values: NDArrayBackedExtensionArray,
        name: Hashable = None,
    ):
        result = super()._simple_new(values, name)

        # For groupby perf. See note in indexes/base about _index_data
        result._index_data = values._ndarray

        return result
