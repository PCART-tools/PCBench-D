    def get_result(self):
        # TODO: find a better way than this masking business

        values, value_mask = self.get_new_values()
        columns = self.get_new_columns()
        index = self.get_new_index()

        # filter out missing levels
        if values.shape[1] > 0:
            col_inds, obs_ids = _compress_group_index(self.sorted_labels[-1])
            # rare case, level values not observed
            if len(obs_ids) < self.full_shape[1]:
                inds = (value_mask.sum(0) > 0).nonzero()[0]
                values = com.take_nd(values, inds, axis=1)
                columns = columns[inds]

        # we might have a missing index
        if len(index) != values.shape[0]:
            mask = isnull(index)
            if mask.any():
                l = np.arange(len(index))
                values, orig_values = (np.empty((len(index), values.shape[1])),
                                       values)
                values.fill(np.nan)
                values_indexer = com._ensure_int64(l[~mask])
                for i, j in enumerate(values_indexer):
                    values[j] = orig_values[i]
            else:
                index = index.take(self.unique_groups)

        return DataFrame(values, index=index, columns=columns)
