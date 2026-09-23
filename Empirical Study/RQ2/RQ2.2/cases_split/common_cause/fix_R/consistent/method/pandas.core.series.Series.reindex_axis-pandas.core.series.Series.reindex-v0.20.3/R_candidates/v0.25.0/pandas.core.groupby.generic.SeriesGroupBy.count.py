    def count(self):
        """
        Compute count of group, excluding missing values.

        Returns
        -------
        Series
            Count of values within each group.
        """
        ids, _, ngroups = self.grouper.group_info
        val = self.obj._internal_get_values()

        mask = (ids != -1) & ~isna(val)
        ids = ensure_platform_int(ids)
        minlength = ngroups or 0
        out = np.bincount(ids[mask], minlength=minlength)

        return Series(
            out,
            index=self.grouper.result_index,
            name=self._selection_name,
            dtype="int64",
        )
