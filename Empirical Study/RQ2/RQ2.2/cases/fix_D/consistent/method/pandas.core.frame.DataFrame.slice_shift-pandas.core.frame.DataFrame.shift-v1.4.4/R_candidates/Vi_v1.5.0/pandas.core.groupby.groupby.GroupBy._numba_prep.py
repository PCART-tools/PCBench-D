    @final
    def _numba_prep(self, data):
        ids, _, ngroups = self.grouper.group_info
        sorted_index = get_group_index_sorter(ids, ngroups)
        sorted_ids = algorithms.take_nd(ids, sorted_index, allow_fill=False)

        sorted_data = data.take(sorted_index, axis=self.axis).to_numpy()
        if len(self.grouper.groupings) > 1:
            raise NotImplementedError(
                "More than 1 grouping labels are not supported with engine='numba'"
            )
        # GH 46867
        index_data = data.index
        if isinstance(index_data, MultiIndex):
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
