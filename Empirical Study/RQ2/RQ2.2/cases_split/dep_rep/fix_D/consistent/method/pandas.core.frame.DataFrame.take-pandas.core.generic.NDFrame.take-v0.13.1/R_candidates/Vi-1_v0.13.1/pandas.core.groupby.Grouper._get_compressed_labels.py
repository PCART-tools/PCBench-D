    def _get_compressed_labels(self):
        all_labels = [ping.labels for ping in self.groupings]
        if self._overflow_possible:
            tups = lib.fast_zip(all_labels)
            labs, uniques = algos.factorize(tups)

            if self.sort:
                uniques, labs = _reorder_by_uniques(uniques, labs)

            return labs, uniques
        else:
            if len(all_labels) > 1:
                group_index = get_group_index(all_labels, self.shape)
                comp_ids, obs_group_ids = _compress_group_index(group_index)
            else:
                ping = self.groupings[0]
                comp_ids = ping.labels
                obs_group_ids = np.arange(len(ping.group_index))
                self.compressed = False
                self._filter_empty_groups = False

            return comp_ids, obs_group_ids
