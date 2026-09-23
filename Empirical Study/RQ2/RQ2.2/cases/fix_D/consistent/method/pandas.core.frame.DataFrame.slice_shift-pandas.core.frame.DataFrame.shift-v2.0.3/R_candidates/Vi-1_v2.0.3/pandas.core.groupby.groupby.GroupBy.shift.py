    @final
    @Substitution(name="groupby")
    def shift(self, periods: int = 1, freq=None, axis: Axis = 0, fill_value=None):
        """
        Shift each group by periods observations.

        If freq is passed, the index will be increased using the periods and the freq.

        Parameters
        ----------
        periods : int, default 1
            Number of periods to shift.
        freq : str, optional
            Frequency string.
        axis : axis to shift, default 0
            Shift direction.
        fill_value : optional
            The scalar value to use for newly introduced missing values.

        Returns
        -------
        Series or DataFrame
            Object shifted within each group.

        See Also
        --------
        Index.shift : Shift values of Index.
        """
        if freq is not None or axis != 0:
            f = lambda x: x.shift(periods, freq, axis, fill_value)
            return self._python_apply_general(f, self._selected_obj, is_transform=True)

        ids, _, ngroups = self.grouper.group_info
        res_indexer = np.zeros(len(ids), dtype=np.int64)

        libgroupby.group_shift_indexer(res_indexer, ids, ngroups, periods)

        obj = self._obj_with_exclusions

        res = obj._reindex_with_indexers(
            {self.axis: (obj.axes[self.axis], res_indexer)},
            fill_value=fill_value,
            allow_dups=True,
        )
        return res
