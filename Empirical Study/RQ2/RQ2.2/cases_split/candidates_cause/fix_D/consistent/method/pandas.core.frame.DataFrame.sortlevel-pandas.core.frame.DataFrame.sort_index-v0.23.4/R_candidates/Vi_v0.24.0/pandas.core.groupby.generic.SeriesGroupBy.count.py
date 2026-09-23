    def count(self):
        """ Compute count of group, excluding missing values """
        ids, _, ngroups = self.grouper.group_info
        val = self.obj.get_values()

        mask = (ids != -1) & ~isna(val)
        ids = ensure_platform_int(ids)
        minlength = ngroups or (None if _np_version_under1p13 else 0)
        out = np.bincount(ids[mask], minlength=minlength)

        return Series(out,
                      index=self.grouper.result_index,
                      name=self._selection_name,
                      dtype='int64')
