    def get_group_levels(self):
        if not self.compressed and len(self.groupings) == 1:
            return [self.groupings[0].group_index]

        name_list = []
        for ping, labels in zip(self.groupings, self.recons_labels):
            labels = com._ensure_platform_int(labels)
            levels = ping.group_index.take(labels)

            name_list.append(levels)

        return name_list
