    def get_result(self, copy: bool = True) -> DataFrame:
        if self.indicator:
            self.left, self.right = self._indicator_pre_merge(self.left, self.right)

        join_index, left_indexer, right_indexer = self._get_join_info()

        result = self._reindex_and_concat(
            join_index, left_indexer, right_indexer, copy=copy
        )
        result = result.__finalize__(self, method=self._merge_type)

        if self.indicator:
            result = self._indicator_post_merge(result)

        self._maybe_add_join_keys(result, left_indexer, right_indexer)

        self._maybe_restore_index_levels(result)

        self._maybe_drop_cross_column(result, self._cross)

        return result.__finalize__(self, method="merge")
