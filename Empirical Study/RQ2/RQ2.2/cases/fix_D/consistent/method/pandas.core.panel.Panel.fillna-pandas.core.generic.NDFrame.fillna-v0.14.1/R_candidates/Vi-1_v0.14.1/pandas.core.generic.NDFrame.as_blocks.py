    def as_blocks(self):
        """
        Convert the frame to a dict of dtype -> Constructor Types that each has
        a homogeneous dtype.

        are presented in sorted order unless a specific list of columns is
        provided.

        NOTE: the dtypes of the blocks WILL BE PRESERVED HERE (unlike in
              as_matrix)

        Parameters
        ----------
        columns : array-like
            Specific column order

        Returns
        -------
        values : a list of Object
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
