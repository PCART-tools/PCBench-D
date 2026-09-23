    def get_result(self):
        if self.indicator:
            self.left, self.right = self._indicator_pre_merge(
                self.left, self.right)

        join_index, left_indexer, right_indexer = self._get_join_info()

        ldata, rdata = self.left._data, self.right._data
        lsuf, rsuf = self.suffixes

        llabels, rlabels = items_overlap_with_suffix(ldata.items, lsuf,
                                                     rdata.items, rsuf)

        lindexers = {1: left_indexer} if left_indexer is not None else {}
        rindexers = {1: right_indexer} if right_indexer is not None else {}

        result_data = concatenate_block_managers(
            [(ldata, lindexers), (rdata, rindexers)],
            axes=[llabels.append(rlabels), join_index],
            concat_axis=0, copy=self.copy)

        typ = self.left._constructor
        result = typ(result_data).__finalize__(self, method=self._merge_type)

        if self.indicator:
            result = self._indicator_post_merge(result)

        self._maybe_add_join_keys(result, left_indexer, right_indexer)

        return result
