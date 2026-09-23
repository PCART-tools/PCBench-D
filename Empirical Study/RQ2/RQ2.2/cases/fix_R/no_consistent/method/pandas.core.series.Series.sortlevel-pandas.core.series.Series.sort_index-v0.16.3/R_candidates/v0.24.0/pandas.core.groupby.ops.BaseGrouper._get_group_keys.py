    def _get_group_keys(self):
        if len(self.groupings) == 1:
            return self.levels[0]
        else:
            comp_ids, _, ngroups = self.group_info

            # provide "flattened" iterator for multi-group setting
            return get_flattened_iterator(comp_ids,
                                          ngroups,
                                          self.levels,
                                          self.labels)
