    def _aggregate(self, result, counts, values, agg_func, is_numeric):
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

        return result
