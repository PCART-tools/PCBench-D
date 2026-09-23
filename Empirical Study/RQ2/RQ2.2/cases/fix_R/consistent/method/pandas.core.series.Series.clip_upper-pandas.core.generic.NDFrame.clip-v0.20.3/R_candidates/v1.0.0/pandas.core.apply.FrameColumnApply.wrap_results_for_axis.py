    def wrap_results_for_axis(
        self, results: ResType, res_index: "Index"
    ) -> Union["Series", "DataFrame"]:
        """ return the results for the columns """
        result: Union["Series", "DataFrame"]

        # we have requested to expand
        if self.result_type == "expand":
            result = self.infer_to_same_shape(results, res_index)

        # we have a non-series and don't want inference
        elif not isinstance(results[0], ABCSeries):
            from pandas import Series

            result = Series(results)
            result.index = res_index

        # we may want to infer results
        else:
            result = self.infer_to_same_shape(results, res_index)

        return result
