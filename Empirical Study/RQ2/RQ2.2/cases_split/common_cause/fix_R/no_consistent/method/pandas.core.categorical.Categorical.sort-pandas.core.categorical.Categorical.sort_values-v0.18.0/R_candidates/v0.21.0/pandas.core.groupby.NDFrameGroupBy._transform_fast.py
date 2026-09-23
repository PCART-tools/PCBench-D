    def _transform_fast(self, result, obj):
        """
        Fast transform path for aggregations
        """
        # if there were groups with no observations (Categorical only?)
        # try casting data to original dtype
        cast = (self.size().fillna(0) > 0).any()

        # for each col, reshape to to size of original frame
        # by take operation
        ids, _, ngroup = self.grouper.group_info
        output = []
        for i, _ in enumerate(result.columns):
            res = algorithms.take_1d(result.iloc[:, i].values, ids)
            if cast:
                res = self._try_cast(res, obj.iloc[:, i])
            output.append(res)

        return DataFrame._from_arrays(output, columns=result.columns,
                                      index=obj.index)
