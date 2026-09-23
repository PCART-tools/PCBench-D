    def _get_join_target(self) -> ArrayLike:
        """
        Get the ndarray or ExtensionArray that we can pass to the join
        functions.
        """
        if isinstance(self._values, BaseMaskedArray):
            # This is only used if our array is monotonic, so no NAs present
            return self._values._data
        elif isinstance(self._values, ArrowExtensionArray):
            # This is only used if our array is monotonic, so no missing values
            # present
            return self._values.to_numpy()
        return self._get_engine_target()
