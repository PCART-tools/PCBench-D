    def _iterate_column_groupbys(self, obj: DataFrame | Series):
        for i, colname in enumerate(obj.columns):
            yield colname, SeriesGroupBy(
                obj.iloc[:, i],
                selection=colname,
                grouper=self.grouper,
                exclusions=self.exclusions,
                observed=self.observed,
            )
