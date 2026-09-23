    def _wrap_agged_blocks(self, blocks: "Sequence[Block]", items: Index) -> DataFrame:
        if not self.as_index:
            index = np.arange(blocks[0].values.shape[-1])
            mgr = BlockManager(blocks, axes=[items, index])
            result = DataFrame(mgr)

            self._insert_inaxis_grouper_inplace(result)
            result = result._consolidate()
        else:
            index = self.grouper.result_index
            mgr = BlockManager(blocks, axes=[items, index])
            result = DataFrame(mgr)

        if self.axis == 1:
            result = result.T

        return self._reindex_output(result)._convert(datetime=True)
