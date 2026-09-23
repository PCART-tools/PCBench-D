    def _iterate_column_groupbys(self):
        for i, colname in enumerate(self._selected_obj.columns):
            yield colname, SeriesGroupBy(self._selected_obj.iloc[:, i],
                                         selection=colname,
                                         grouper=self.grouper,
                                         exclusions=self.exclusions)
