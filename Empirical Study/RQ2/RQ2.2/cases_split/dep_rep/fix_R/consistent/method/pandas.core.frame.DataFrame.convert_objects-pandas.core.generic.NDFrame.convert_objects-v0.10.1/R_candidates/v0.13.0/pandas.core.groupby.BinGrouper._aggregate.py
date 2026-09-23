    def _aggregate(self, result, counts, values, how, is_numeric=True):

        agg_func, dtype = self._get_aggregate_function(how, values)
        trans_func = self._cython_transforms.get(how, lambda x: x)

        if values.ndim > 3:
            # punting for now
            raise NotImplementedError
        elif values.ndim > 2:
            for i, chunk in enumerate(values.transpose(2, 0, 1)):
                agg_func(result[:, :, i], counts, chunk, self.bins)
        else:
            agg_func(result, counts, values, self.bins)

        return trans_func(result)
