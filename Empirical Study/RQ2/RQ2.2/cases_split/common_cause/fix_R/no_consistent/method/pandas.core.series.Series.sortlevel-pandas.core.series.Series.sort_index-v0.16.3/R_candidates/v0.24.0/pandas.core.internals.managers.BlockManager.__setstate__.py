    def __setstate__(self, state):
        def unpickle_block(values, mgr_locs):
            return make_block(values, placement=mgr_locs)

        if (isinstance(state, tuple) and len(state) >= 4 and
                '0.14.1' in state[3]):
            state = state[3]['0.14.1']
            self.axes = [ensure_index(ax) for ax in state['axes']]
            self.blocks = tuple(unpickle_block(b['values'], b['mgr_locs'])
                                for b in state['blocks'])
        else:
            # discard anything after 3rd, support beta pickling format for a
            # little while longer
            ax_arrays, bvalues, bitems = state[:3]

            self.axes = [ensure_index(ax) for ax in ax_arrays]

            if len(bitems) == 1 and self.axes[0].equals(bitems[0]):
                # This is a workaround for pre-0.14.1 pickles that didn't
                # support unpickling multi-block frames/panels with non-unique
                # columns/items, because given a manager with items ["a", "b",
                # "a"] there's no way of knowing which block's "a" is where.
                #
                # Single-block case can be supported under the assumption that
                # block items corresponded to manager items 1-to-1.
                all_mgr_locs = [slice(0, len(bitems[0]))]
            else:
                all_mgr_locs = [self.axes[0].get_indexer(blk_items)
                                for blk_items in bitems]

            self.blocks = tuple(
                unpickle_block(values, mgr_locs)
                for values, mgr_locs in zip(bvalues, all_mgr_locs))

        self._post_setstate()
