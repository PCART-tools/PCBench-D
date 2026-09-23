    def __getstate__(self):
        block_values = [b.values for b in self.blocks]
        block_items = [self.items[b.mgr_locs.indexer] for b in self.blocks]
        axes_array = [ax for ax in self.axes]

        extra_state = {
            '0.14.1': {
                'axes': axes_array,
                'blocks': [dict(values=b.values, mgr_locs=b.mgr_locs.indexer)
                           for b in self.blocks]
            }
        }

        # First three elements of the state are to maintain forward
        # compatibility with 0.13.1.
        return axes_array, block_values, block_items, extra_state
