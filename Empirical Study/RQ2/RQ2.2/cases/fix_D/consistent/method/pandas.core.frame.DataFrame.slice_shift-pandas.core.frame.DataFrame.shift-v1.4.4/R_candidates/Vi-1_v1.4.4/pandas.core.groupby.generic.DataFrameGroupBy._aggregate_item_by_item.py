    def _aggregate_item_by_item(self, func, *args, **kwargs) -> DataFrame:
        # only for axis==0
        # tests that get here with non-unique cols:
        #  test_resample_with_timedelta_yields_no_empty_groups,
        #  test_resample_apply_product

        obj = self._obj_with_exclusions
        result: dict[int, NDFrame] = {}

        for i, (item, sgb) in enumerate(self._iterate_column_groupbys(obj)):
            result[i] = sgb.aggregate(func, *args, **kwargs)

        res_df = self.obj._constructor(result)
        res_df.columns = obj.columns
        return res_df
