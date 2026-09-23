    def _get_unstack_items(self, unstacker, new_columns):
        """
        Get the placement, values, and mask for a Block unstack.

        This is shared between ObjectBlock and ExtensionBlock. They
        differ in that ObjectBlock passes the values, while ExtensionBlock
        passes the dummy ndarray of positions to be used by a take
        later.

        Parameters
        ----------
        unstacker : pandas.core.reshape.reshape._Unstacker
        new_columns : Index
            All columns of the unstacked BlockManager.

        Returns
        -------
        new_placement : ndarray[int]
            The placement of the new columns in `new_columns`.
        new_values : Union[ndarray, ExtensionArray]
            The first return value from _Unstacker.get_new_values.
        mask : ndarray[bool]
            The second return value from _Unstacker.get_new_values.
        """
        # shared with ExtensionBlock
        new_items = unstacker.get_new_columns()
        new_placement = new_columns.get_indexer(new_items)
        new_values, mask = unstacker.get_new_values()

        mask = mask.any(0)
        return new_placement, new_values, mask
