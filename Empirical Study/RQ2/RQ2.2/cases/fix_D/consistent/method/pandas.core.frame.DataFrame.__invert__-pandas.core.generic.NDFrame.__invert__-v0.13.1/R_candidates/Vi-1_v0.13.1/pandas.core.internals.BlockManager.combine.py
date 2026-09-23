    def combine(self, blocks):
        """ return a new manager with the blocks """
        indexer = np.sort(np.concatenate([b.ref_locs for b in blocks]))
        new_items = self.items.take(indexer)

        new_blocks = []
        for b in blocks:
            b = b.copy(deep=False)
            b.ref_items = new_items
            new_blocks.append(b)
        new_axes = list(self.axes)
        new_axes[0] = new_items
        return self.__class__(new_blocks, new_axes, do_integrity_check=False)
