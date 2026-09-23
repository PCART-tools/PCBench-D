    def _apply_to_column_groupbys(self, func, obj: DataFrame) -> DataFrame:
        from pandas.core.reshape.concat import concat

        columns = obj.columns
        results = [
            func(col_groupby) for _, col_groupby in self._iterate_column_groupbys(obj)
        ]

        if not len(results):
            # concat would raise
            return DataFrame([], columns=columns, index=self.grouper.result_index)
        else:
            return concat(results, keys=columns, axis=1)
