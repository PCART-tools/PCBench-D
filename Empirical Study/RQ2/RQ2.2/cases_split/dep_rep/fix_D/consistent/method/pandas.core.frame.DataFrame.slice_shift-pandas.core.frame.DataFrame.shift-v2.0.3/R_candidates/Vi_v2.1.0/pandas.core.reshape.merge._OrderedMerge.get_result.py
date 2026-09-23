    def get_result(self, copy: bool | None = True) -> DataFrame:
        join_index, left_indexer, right_indexer = self._get_join_info()

        left_join_indexer: npt.NDArray[np.intp] | None
        right_join_indexer: npt.NDArray[np.intp] | None

        if self.fill_method == "ffill":
            if left_indexer is None:
                raise TypeError("left_indexer cannot be None")
            left_indexer = cast("npt.NDArray[np.intp]", left_indexer)
            right_indexer = cast("npt.NDArray[np.intp]", right_indexer)
            left_join_indexer = libjoin.ffill_indexer(left_indexer)
            right_join_indexer = libjoin.ffill_indexer(right_indexer)
        else:
            left_join_indexer = left_indexer
            right_join_indexer = right_indexer

        result = self._reindex_and_concat(
            join_index, left_join_indexer, right_join_indexer, copy=copy
        )
        self._maybe_add_join_keys(result, left_indexer, right_indexer)

        return result
