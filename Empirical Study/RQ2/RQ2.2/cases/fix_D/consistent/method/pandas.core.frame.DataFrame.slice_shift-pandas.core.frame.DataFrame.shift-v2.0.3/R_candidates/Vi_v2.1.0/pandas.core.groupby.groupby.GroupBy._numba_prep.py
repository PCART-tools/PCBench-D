    @final
    def _numba_prep(self, data: DataFrame):
        ids, _, ngroups = self.grouper.group_info
        sorted_index = self.grouper._sort_idx
        sorted_ids = self.grouper._sorted_ids

        sorted_data = data.take(sorted_index, axis=self.axis).to_numpy()
        # GH 46867
        index_data = data.index
        if isinstance(index_data, MultiIndex):
            if len(self.grouper.groupings) > 1:
                raise NotImplementedError(
                    "Grouping with more than 1 grouping labels and "
                    "a MultiIndex is not supported with engine='numba'"
                )
            group_key = self.grouper.groupings[0].name
            index_data = index_data.get_level_values(group_key)
        sorted_index_data = index_data.take(sorted_index).to_numpy()

        starts, ends = lib.generate_slices(sorted_ids, ngroups)
        return (
            starts,
            ends,
            sorted_index_data,
            sorted_data,
        )
