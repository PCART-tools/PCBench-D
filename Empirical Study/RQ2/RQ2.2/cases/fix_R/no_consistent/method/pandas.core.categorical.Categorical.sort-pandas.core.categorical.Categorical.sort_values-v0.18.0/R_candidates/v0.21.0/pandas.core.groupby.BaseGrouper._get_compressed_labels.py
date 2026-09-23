    def _get_compressed_labels(self):
        all_labels = [ping.labels for ping in self.groupings]
        if len(all_labels) > 1:
            group_index = get_group_index(all_labels, self.shape,
                                          sort=True, xnull=True)
            return compress_group_index(group_index, sort=self.sort)

        ping = self.groupings[0]
        return ping.labels, np.arange(len(ping.group_index))
