    def _make_selectors(self):
        new_levels = self.new_index_levels

        # make the mask
        remaining_labels = self.sorted_labels[:-1]
        level_sizes = [len(x) for x in new_levels]

        comp_index, obs_ids = get_compressed_ids(remaining_labels, level_sizes)
        ngroups = len(obs_ids)

        comp_index = ensure_platform_int(comp_index)
        stride = self.index.levshape[self.level] + self.lift
        self.full_shape = ngroups, stride

        selector = self.sorted_labels[-1] + stride * comp_index + self.lift
        mask = np.zeros(np.prod(self.full_shape), dtype=bool)
        mask.put(selector, True)

        if mask.sum() < len(self.index):
            raise ValueError('Index contains duplicate entries, '
                             'cannot reshape')

        self.group_index = comp_index
        self.mask = mask
        self.unique_groups = obs_ids
        self.compressor = comp_index.searchsorted(np.arange(ngroups))
