    def _unstack(self, unstacker_func, new_columns):
        """Return a list of unstacked blocks of self

        Parameters
        ----------
        unstacker_func : callable
            Partially applied unstacker.
        new_columns : Index
            All columns of the unstacked BlockManager.

        Returns
        -------
        blocks : list of Block
            New blocks of unstacked values.
        mask : array_like of bool
            The mask of columns of `blocks` we should keep.
        """
        # NonConsolidatable blocks can have a single item only, so we return
        # one block per item
        unstacker = unstacker_func(self.values.T)
        new_items = unstacker.get_new_columns()
        new_placement = new_columns.get_indexer(new_items)
        new_values, mask = unstacker.get_new_values()

        mask = mask.any(0)
        new_values = new_values.T[mask]
        new_placement = new_placement[mask]

        blocks = [self.make_block_same_class(vals, [place])
                  for vals, place in zip(new_values, new_placement)]
        return blocks, mask
