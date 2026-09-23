    def wrap_results_for_axis(
        self, results: ResType, res_index: "Index"
    ) -> "DataFrame":
        """ return the results for the rows """

        result = self.obj._constructor(data=results)

        if not isinstance(results[0], ABCSeries):
            if len(result.index) == len(self.res_columns):
                result.index = self.res_columns

        if len(result.columns) == len(res_index):
            result.columns = res_index

        return result
