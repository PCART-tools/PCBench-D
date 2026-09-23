    def merge(self, other, lsuffix='', rsuffix=''):
        if not self._is_indexed_like(other):
            raise AssertionError('Must have same axes to merge managers')

        l, r = items_overlap_with_suffix(left=self.items, lsuffix=lsuffix,
                                         right=other.items, rsuffix=rsuffix)
        new_items = _concat_indexes([l, r])

        new_blocks = [blk.copy(deep=False)
                      for blk in self.blocks]

        offset = self.shape[0]
        for blk in other.blocks:
            blk = blk.copy(deep=False)
            blk.mgr_locs = blk.mgr_locs.add(offset)
            new_blocks.append(blk)

        new_axes = list(self.axes)
        new_axes[0] = new_items

        return self.__class__(_consolidate(new_blocks), new_axes)
