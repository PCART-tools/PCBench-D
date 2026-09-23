    def _aggregate(self, result, counts, values, how, is_numeric):
        agg_func, dtype = self._get_aggregate_function(how, values)
        trans_func = self._cython_transforms.get(how, lambda x: x)

        comp_ids, _, ngroups = self.group_info
        if values.ndim > 3:
            # punting for now
            raise NotImplementedError
        elif values.ndim > 2:
            for i, chunk in enumerate(values.transpose(2, 0, 1)):

                chunk = chunk.squeeze()
                agg_func(result[:, :, i], counts, chunk, comp_ids)
        else:
            agg_func(result, counts, values, comp_ids)

        return trans_func(result)
