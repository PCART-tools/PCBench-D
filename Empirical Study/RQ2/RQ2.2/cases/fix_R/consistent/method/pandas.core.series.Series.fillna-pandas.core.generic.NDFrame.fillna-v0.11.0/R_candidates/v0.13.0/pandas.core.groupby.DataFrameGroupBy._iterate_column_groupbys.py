    def _iterate_column_groupbys(self):
        for i, colname in enumerate(self.obj.columns):
            yield colname, SeriesGroupBy(self.obj.iloc[:, i],
                                         selection=colname,
                                         grouper=self.grouper,
                                         exclusions=self.exclusions)
