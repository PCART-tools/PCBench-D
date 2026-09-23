    def _unstack(self, unstacker_func, new_columns, n_rows, fill_value):
        """Return a list of unstacked blocks of self

        Parameters
        ----------
        unstacker_func : callable
            Partially applied unstacker.
        new_columns : Index
            All columns of the unstacked BlockManager.
        n_rows : int
            Only used in ExtensionBlock.unstack
        fill_value : int
            Only used in ExtensionBlock.unstack

        Returns
        -------
        blocks : list of Block
            New blocks of unstacked values.
        mask : array_like of bool
            The mask of columns of `blocks` we should keep.
        """
        unstacker = unstacker_func(self.values.T)
        new_items = unstacker.get_new_columns()
        new_placement = new_columns.get_indexer(new_items)
        new_values, mask = unstacker.get_new_values()

        mask = mask.any(0)
        new_values = new_values.T[mask]
        new_placement = new_placement[mask]

        blocks = [make_block(new_values, placement=new_placement)]
        return blocks, mask
