    def _make_sorted_values(self, values: np.ndarray) -> np.ndarray:
        indexer, _ = self._indexer_and_to_sort

        sorted_values = algos.take_nd(values, indexer, axis=0)
        return sorted_values
