    @property
    def recons_labels(self):
        comp_ids, obs_ids, _ = self.group_info
        labels = (ping.labels for ping in self.groupings)
        return decons_obs_group_ids(comp_ids,
                obs_ids, self.shape, labels, xnull=True)
