    @final
    def _get_compressed_codes(
        self,
    ) -> tuple[npt.NDArray[np.signedinteger], npt.NDArray[np.intp]]:
        # The first returned ndarray may have any signed integer dtype
        if len(self.groupings) > 1:
            group_index = get_group_index(self.codes, self.shape, sort=True, xnull=True)
            return compress_group_index(group_index, sort=self._sort)
            # FIXME: compress_group_index's second return value is int64, not intp

        ping = self.groupings[0]
        return ping.codes, np.arange(len(ping.group_index), dtype=np.intp)
