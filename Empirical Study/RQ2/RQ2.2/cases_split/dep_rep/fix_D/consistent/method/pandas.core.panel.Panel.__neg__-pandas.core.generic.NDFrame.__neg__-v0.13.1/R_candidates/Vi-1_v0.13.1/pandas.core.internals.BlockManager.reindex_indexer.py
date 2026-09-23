    def reindex_indexer(self, new_axis, indexer, axis=1, fill_value=None,
                        allow_dups=False):
        """
        pandas-indexer with -1's only.
        """
        # trying to reindex on an axis with duplicates
        if not allow_dups and not self.axes[axis].is_unique:
            raise ValueError("cannot reindex from a duplicate axis")

        if not self.is_consolidated():
            self = self.consolidate()

        if axis == 0:
            return self._reindex_indexer_items(new_axis, indexer, fill_value)

        new_blocks = []
        for block in self.blocks:
            newb = block.reindex_axis(
                indexer, axis=axis, fill_value=fill_value)
            new_blocks.append(newb)

        new_axes = list(self.axes)
        new_axes[axis] = new_axis
        return self.__class__(new_blocks, new_axes)
