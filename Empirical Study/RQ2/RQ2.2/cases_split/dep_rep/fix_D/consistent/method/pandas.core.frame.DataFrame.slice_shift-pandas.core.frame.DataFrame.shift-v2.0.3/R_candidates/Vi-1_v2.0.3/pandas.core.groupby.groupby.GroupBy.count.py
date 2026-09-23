    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def count(self) -> NDFrameT:
        """
        Compute count of group, excluding missing values.

        Returns
        -------
        Series or DataFrame
            Count of values within each group.
        """
        data = self._get_data_to_aggregate()
        ids, _, ngroups = self.grouper.group_info
        mask = ids != -1

        is_series = data.ndim == 1

        def hfunc(bvalues: ArrayLike) -> ArrayLike:
            # TODO(EA2D): reshape would not be necessary with 2D EAs
            if bvalues.ndim == 1:
                # EA
                masked = mask & ~isna(bvalues).reshape(1, -1)
            else:
                masked = mask & ~isna(bvalues)

            counted = lib.count_level_2d(masked, labels=ids, max_bin=ngroups)
            if is_series:
                assert counted.ndim == 2
                assert counted.shape[0] == 1
                return counted[0]
            return counted

        new_mgr = data.grouped_reduce(hfunc)
        new_obj = self._wrap_agged_manager(new_mgr)

        # If we are grouping on categoricals we want unobserved categories to
        # return zero, rather than the default of NaN which the reindexing in
        # _wrap_aggregated_output() returns. GH 35028
        # e.g. test_dataframe_groupby_on_2_categoricals_when_observed_is_false
        with com.temp_setattr(self, "observed", True):
            result = self._wrap_aggregated_output(new_obj)

        return self._reindex_output(result, fill_value=0)
