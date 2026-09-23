    def get_result(self) -> DataFrame:
        join_index, left_indexer, right_indexer = self._get_join_info()

        llabels, rlabels = _items_overlap_with_suffix(
            self.left._info_axis, self.right._info_axis, self.suffixes
        )

        left_join_indexer: np.ndarray | None
        right_join_indexer: np.ndarray | None

        if self.fill_method == "ffill":
            if left_indexer is None:
                raise TypeError("left_indexer cannot be None")
            left_indexer, right_indexer = cast(np.ndarray, left_indexer), cast(
                np.ndarray, right_indexer
            )
            left_join_indexer = libjoin.ffill_indexer(left_indexer)
            right_join_indexer = libjoin.ffill_indexer(right_indexer)
        else:
            left_join_indexer = left_indexer
            right_join_indexer = right_indexer

        lindexers = {1: left_join_indexer} if left_join_indexer is not None else {}
        rindexers = {1: right_join_indexer} if right_join_indexer is not None else {}

        result_data = concatenate_managers(
            [(self.left._mgr, lindexers), (self.right._mgr, rindexers)],
            axes=[llabels.append(rlabels), join_index],
            concat_axis=0,
            copy=self.copy,
        )

        typ = self.left._constructor
        result = typ(result_data)

        self._maybe_add_join_keys(result, left_indexer, right_indexer)

        return result
