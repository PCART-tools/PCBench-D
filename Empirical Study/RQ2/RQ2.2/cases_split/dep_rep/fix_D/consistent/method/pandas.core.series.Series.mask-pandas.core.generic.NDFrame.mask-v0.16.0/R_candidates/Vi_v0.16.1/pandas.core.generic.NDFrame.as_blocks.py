    def as_blocks(self):
        """
        Convert the frame to a dict of dtype -> Constructor Types that each has
        a homogeneous dtype.

        NOTE: the dtypes of the blocks WILL BE PRESERVED HERE (unlike in
              as_matrix)

        Returns
        -------
        values : a dict of dtype -> Constructor Types
        """
        self._consolidate_inplace()

        bd = {}
        for b in self._data.blocks:
            bd.setdefault(str(b.dtype), []).append(b)

        result = {}
        for dtype, blocks in bd.items():
            # Must combine even after consolidation, because there may be
            # sparse items which are never consolidated into one block.
            combined = self._data.combine(blocks, copy=True)
            result[dtype] = self._constructor(combined).__finalize__(self)

        return result
