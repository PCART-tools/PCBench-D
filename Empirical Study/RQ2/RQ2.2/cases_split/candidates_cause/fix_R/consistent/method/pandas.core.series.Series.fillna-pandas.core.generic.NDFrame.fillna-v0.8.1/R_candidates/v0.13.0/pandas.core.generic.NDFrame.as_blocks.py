    def as_blocks(self, columns=None):
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

        bd = dict()
        for b in self._data.blocks:
            b = b.reindex_items_from(columns or b.items)
            bd[str(b.dtype)] = self._constructor(
                BlockManager([b], [b.items, self.index])).__finalize__(self)
        return bd
