    def get_group_levels(self):
        obs_ids = self.group_info[1]

        if not self.compressed and len(self.groupings) == 1:
            return [self.groupings[0].group_index]

        if self._overflow_possible:
            recons_labels = [np.array(x) for x in zip(*obs_ids)]
        else:
            recons_labels = decons_group_index(obs_ids, self.shape)

        name_list = []
        for ping, labels in zip(self.groupings, recons_labels):
            labels = com._ensure_platform_int(labels)
            levels = ping.group_index.take(labels)

            name_list.append(levels)

        return name_list
