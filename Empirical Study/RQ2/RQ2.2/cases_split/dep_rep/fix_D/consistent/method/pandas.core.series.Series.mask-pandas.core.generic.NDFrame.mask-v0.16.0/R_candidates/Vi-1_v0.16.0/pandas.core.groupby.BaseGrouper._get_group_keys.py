    def _get_group_keys(self):
        if len(self.groupings) == 1:
            return self.levels[0]
        else:
            comp_ids, _, ngroups = self.group_info
            # provide "flattened" iterator for multi-group setting
            mapper = _KeyMapper(comp_ids, ngroups, self.labels, self.levels)
            return [mapper.get_key(i) for i in range(ngroups)]
