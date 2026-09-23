    def _get_compressed_codes(self) -> Tuple[np.ndarray, np.ndarray]:
        all_codes = self.codes
        if len(all_codes) > 1:
            group_index = get_group_index(all_codes, self.shape, sort=True, xnull=True)
            return compress_group_index(group_index, sort=self.sort)

        ping = self.groupings[0]
        return ping.codes, np.arange(len(ping.group_index))
