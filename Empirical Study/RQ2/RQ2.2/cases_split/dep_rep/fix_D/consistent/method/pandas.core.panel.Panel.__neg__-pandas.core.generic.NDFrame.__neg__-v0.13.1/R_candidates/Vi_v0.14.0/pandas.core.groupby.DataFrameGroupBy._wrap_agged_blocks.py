    def _wrap_agged_blocks(self, items, blocks):
        if not self.as_index:
            index = np.arange(blocks[0].values.shape[1])
            mgr = BlockManager(blocks, [items, index])
            result = DataFrame(mgr)

            group_levels = self.grouper.get_group_levels()
            zipped = zip(self.grouper.names, group_levels)

            for i, (name, labels) in enumerate(zipped):
                result.insert(i, name, labels)
            result = result.consolidate()
        else:
            index = self.grouper.result_index
            mgr = BlockManager(blocks, [items, index])
            result = DataFrame(mgr)

        if self.axis == 1:
            result = result.T

        return result.convert_objects()
