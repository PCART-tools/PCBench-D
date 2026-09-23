    def unstack(self, unstacker_func, fill_value):
        """Return a blockmanager with all blocks unstacked.

        Parameters
        ----------
        unstacker_func : callable
            A (partially-applied) ``pd.core.reshape._Unstacker`` class.
        fill_value : Any
            fill_value for newly introduced missing values.

        Returns
        -------
        unstacked : BlockManager
        """
        n_rows = self.shape[-1]
        dummy = unstacker_func(np.empty((0, 0)), value_columns=self.items)
        new_columns = dummy.get_new_columns()
        new_index = dummy.get_new_index()
        new_blocks = []
        columns_mask = []

        for blk in self.blocks:
            blocks, mask = blk._unstack(
                partial(unstacker_func, value_columns=self.items[blk.mgr_locs.indexer]),
                new_columns,
                n_rows,
                fill_value,
            )

            new_blocks.extend(blocks)
            columns_mask.extend(mask)

        new_columns = new_columns[columns_mask]

        bm = BlockManager(new_blocks, [new_columns, new_index])
        return bm
