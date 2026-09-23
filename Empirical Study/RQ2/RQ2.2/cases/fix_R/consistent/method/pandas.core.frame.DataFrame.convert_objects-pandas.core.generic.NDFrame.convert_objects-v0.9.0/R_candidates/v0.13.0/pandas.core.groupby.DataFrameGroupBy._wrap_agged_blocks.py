    def _wrap_agged_blocks(self, blocks):
        obj = self._obj_with_exclusions

        if self.axis == 0:
            agg_labels = obj.columns
        else:
            agg_labels = obj.index

        if sum(len(x.items) for x in blocks) == len(agg_labels):
            output_keys = agg_labels
        else:
            all_items = []
            for b in blocks:
                all_items.extend(b.items)
            output_keys = agg_labels[agg_labels.isin(all_items)]

            for blk in blocks:
                blk.set_ref_items(output_keys, maybe_rename=False)

        if not self.as_index:
            index = np.arange(blocks[0].values.shape[1])
            mgr = BlockManager(blocks, [output_keys, index])
            result = DataFrame(mgr)

            group_levels = self.grouper.get_group_levels()
            zipped = zip(self.grouper.names, group_levels)

            for i, (name, labels) in enumerate(zipped):
                result.insert(i, name, labels)
            result = result.consolidate()
        else:
            index = self.grouper.result_index
            mgr = BlockManager(blocks, [output_keys, index])
            result = DataFrame(mgr)

        if self.axis == 1:
            result = result.T

        return result.convert_objects()
