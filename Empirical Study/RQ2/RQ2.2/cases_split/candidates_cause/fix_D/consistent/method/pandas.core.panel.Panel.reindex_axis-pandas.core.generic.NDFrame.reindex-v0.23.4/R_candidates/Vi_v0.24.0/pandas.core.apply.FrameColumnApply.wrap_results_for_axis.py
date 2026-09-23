    def wrap_results_for_axis(self):
        """ return the results for the columns """
        results = self.results

        # we have requested to expand
        if self.result_type == 'expand':
            result = self.infer_to_same_shape()

        # we have a non-series and don't want inference
        elif not isinstance(results[0], ABCSeries):
            from pandas import Series
            result = Series(results)
            result.index = self.res_index

        # we may want to infer results
        else:
            result = self.infer_to_same_shape()

        return result
