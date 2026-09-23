    def get_result(self) -> DataFrame:
        if self.indicator:
            self.left, self.right = self._indicator_pre_merge(self.left, self.right)

        join_index, left_indexer, right_indexer = self._get_join_info()

        llabels, rlabels = _items_overlap_with_suffix(
            self.left._info_axis, self.right._info_axis, self.suffixes
        )

        lindexers = {1: left_indexer} if left_indexer is not None else {}
        rindexers = {1: right_indexer} if right_indexer is not None else {}

        result_data = concatenate_managers(
            [(self.left._mgr, lindexers), (self.right._mgr, rindexers)],
            axes=[llabels.append(rlabels), join_index],
            concat_axis=0,
            copy=self.copy,
        )

        typ = self.left._constructor
        result = typ(result_data).__finalize__(self, method=self._merge_type)

        if self.indicator:
            result = self._indicator_post_merge(result)

        self._maybe_add_join_keys(result, left_indexer, right_indexer)

        self._maybe_restore_index_levels(result)

        self._maybe_drop_cross_column(result, self._cross)

        return result.__finalize__(self, method="merge")
