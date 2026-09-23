    def _from_join_target(self, result: np.ndarray) -> ArrayLike:
        """
        Cast the ndarray returned from one of the libjoin.foo_indexer functions
        back to type(self)._data.
        """
        if isinstance(self.values, BaseMaskedArray):
            return type(self.values)(result, np.zeros(result.shape, dtype=np.bool_))
        elif isinstance(self.values, ArrowExtensionArray):
            return type(self.values)._from_sequence(result)
        return result
