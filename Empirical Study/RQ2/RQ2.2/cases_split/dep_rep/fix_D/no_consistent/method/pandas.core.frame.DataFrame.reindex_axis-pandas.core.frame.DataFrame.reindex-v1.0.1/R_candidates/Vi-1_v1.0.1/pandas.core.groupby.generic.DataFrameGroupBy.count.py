    def count(self):
        """
        Compute count of group, excluding missing values.

        Returns
        -------
        DataFrame
            Count of values within each group.
        """
        data = self._get_data_to_aggregate()
        ids, _, ngroups = self.grouper.group_info
        mask = ids != -1

        vals = (
            (mask & ~_isna_ndarraylike(np.atleast_2d(blk.get_values())))
            for blk in data.blocks
        )
        locs = (blk.mgr_locs for blk in data.blocks)

        counted = (
            lib.count_level_2d(x, labels=ids, max_bin=ngroups, axis=1) for x in vals
        )
        blocks = [make_block(val, placement=loc) for val, loc in zip(counted, locs)]

        return self._wrap_agged_blocks(blocks, items=data.items)
