    def _apply_to_column_groupbys(self, func) -> DataFrame:
        from pandas.core.reshape.concat import concat

        obj = self._obj_with_exclusions
        columns = obj.columns
        sgbs = [
            SeriesGroupBy(
                obj.iloc[:, i],
                selection=colname,
                grouper=self.grouper,
                exclusions=self.exclusions,
                observed=self.observed,
            )
            for i, colname in enumerate(obj.columns)
        ]
        results = [func(sgb) for sgb in sgbs]

        if not len(results):
            # concat would raise
            res_df = DataFrame([], columns=columns, index=self.grouper.result_index)
        else:
            res_df = concat(results, keys=columns, axis=1)

        if not self.as_index:
            res_df.index = default_index(len(res_df))
            res_df = self._insert_inaxis_grouper(res_df)
        return res_df
