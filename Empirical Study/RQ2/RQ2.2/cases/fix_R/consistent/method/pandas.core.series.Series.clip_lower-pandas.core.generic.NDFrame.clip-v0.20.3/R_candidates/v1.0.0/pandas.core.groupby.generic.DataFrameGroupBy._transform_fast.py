    def _transform_fast(self, result: DataFrame, func_nm: str) -> DataFrame:
        """
        Fast transform path for aggregations
        """
        # if there were groups with no observations (Categorical only?)
        # try casting data to original dtype
        cast = self._transform_should_cast(func_nm)

        obj = self._obj_with_exclusions

        # for each col, reshape to to size of original frame
        # by take operation
        ids, _, ngroup = self.grouper.group_info
        output = []
        for i, _ in enumerate(result.columns):
            res = algorithms.take_1d(result.iloc[:, i].values, ids)
            # TODO: we have no test cases that get here with EA dtypes;
            #  try_cast may not be needed if EAs never get here
            if cast:
                res = self._try_cast(res, obj.iloc[:, i])
            output.append(res)

        return DataFrame._from_arrays(output, columns=result.columns, index=obj.index)
