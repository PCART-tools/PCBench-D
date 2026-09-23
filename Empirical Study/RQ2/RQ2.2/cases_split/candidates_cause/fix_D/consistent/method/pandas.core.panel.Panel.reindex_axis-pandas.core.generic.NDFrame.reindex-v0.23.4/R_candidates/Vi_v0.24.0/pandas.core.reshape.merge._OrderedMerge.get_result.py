    def get_result(self):
        join_index, left_indexer, right_indexer = self._get_join_info()

        # this is a bit kludgy
        ldata, rdata = self.left._data, self.right._data
        lsuf, rsuf = self.suffixes

        llabels, rlabels = items_overlap_with_suffix(ldata.items, lsuf,
                                                     rdata.items, rsuf)

        if self.fill_method == 'ffill':
            left_join_indexer = libjoin.ffill_indexer(left_indexer)
            right_join_indexer = libjoin.ffill_indexer(right_indexer)
        else:
            left_join_indexer = left_indexer
            right_join_indexer = right_indexer

        lindexers = {
            1: left_join_indexer} if left_join_indexer is not None else {}
        rindexers = {
            1: right_join_indexer} if right_join_indexer is not None else {}

        result_data = concatenate_block_managers(
            [(ldata, lindexers), (rdata, rindexers)],
            axes=[llabels.append(rlabels), join_index],
            concat_axis=0, copy=self.copy)

        typ = self.left._constructor
        result = typ(result_data).__finalize__(self, method=self._merge_type)

        self._maybe_add_join_keys(result, left_indexer, right_indexer)

        return result
