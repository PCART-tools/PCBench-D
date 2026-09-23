    def _apply_to_column_groupbys(self, func):
        from pandas.tools.merge import concat
        return concat(
            (func(col_groupby) for _, col_groupby
             in self._iterate_column_groupbys()),
            keys=self.obj.columns, axis=1)
