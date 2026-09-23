    def combine(self, blocks, copy=True):
        """ return a new manager with the blocks """
        if len(blocks) == 0:
            return self.make_empty()

        # FIXME: optimization potential
        indexer = np.sort(np.concatenate([b.mgr_locs.as_array for b in blocks]))
        inv_indexer = lib.get_reverse_indexer(indexer, self.shape[0])
        new_items = self.items.take(indexer)

        new_blocks = []
        for b in blocks:
            b = b.copy(deep=copy)
            b.mgr_locs = com.take_1d(inv_indexer, b.mgr_locs.as_array, axis=0,
                                     allow_fill=False)
            new_blocks.append(b)

        new_axes = list(self.axes)
        new_axes[0] = new_items
        return self.__class__(new_blocks, new_axes, do_integrity_check=False)
