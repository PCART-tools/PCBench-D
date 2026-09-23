    def count(self):
        """ Compute count of group, excluding missing values """
        ids, _, ngroups = self.grouper.group_info
        val = self.obj.get_values()

        mask = (ids != -1) & ~isnull(val)
        ids = _ensure_platform_int(ids)
        out = np.bincount(ids[mask], minlength=ngroups or None)

        return Series(out,
                      index=self.grouper.result_index,
                      name=self._selection_name,
                      dtype='int64')
