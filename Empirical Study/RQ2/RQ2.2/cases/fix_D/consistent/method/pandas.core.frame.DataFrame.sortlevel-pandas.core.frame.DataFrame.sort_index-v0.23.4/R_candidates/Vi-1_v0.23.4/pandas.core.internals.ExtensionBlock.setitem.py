    def setitem(self, indexer, value, mgr=None):
        """Set the value inplace, returning a same-typed block.

        This differs from Block.setitem by not allowing setitem to change
        the dtype of the Block.

        Parameters
        ----------
        indexer : tuple, list-like, array-like, slice
            The subset of self.values to set
        value : object
            The value being set
        mgr : BlockPlacement, optional

        Returns
        -------
        Block

        Notes
        -----
        `indexer` is a direct slice/positional indexer. `value` must
        be a compatible shape.
        """
        if isinstance(indexer, tuple):
            # we are always 1-D
            indexer = indexer[0]

        check_setitem_lengths(indexer, value, self.values)
        self.values[indexer] = value
        return self
