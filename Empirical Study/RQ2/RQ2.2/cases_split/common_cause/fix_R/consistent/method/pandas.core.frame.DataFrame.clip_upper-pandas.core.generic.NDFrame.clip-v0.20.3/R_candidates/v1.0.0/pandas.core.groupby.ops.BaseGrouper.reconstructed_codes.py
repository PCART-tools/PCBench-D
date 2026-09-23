    @property
    def reconstructed_codes(self) -> List[np.ndarray]:
        codes = self.codes
        comp_ids, obs_ids, _ = self.group_info
        return decons_obs_group_ids(comp_ids, obs_ids, self.shape, codes, xnull=True)
