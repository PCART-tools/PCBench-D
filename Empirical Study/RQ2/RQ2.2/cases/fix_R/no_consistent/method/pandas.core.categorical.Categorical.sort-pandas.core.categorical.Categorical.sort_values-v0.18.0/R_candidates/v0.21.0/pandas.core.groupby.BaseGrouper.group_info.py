    @cache_readonly
    def group_info(self):
        comp_ids, obs_group_ids = self._get_compressed_labels()

        ngroups = len(obs_group_ids)
        comp_ids = _ensure_int64(comp_ids)
        return comp_ids, obs_group_ids, ngroups
