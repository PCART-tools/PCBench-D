    def size(self) -> Series:
        """
        Compute group sizes.
        """
        ids, _, ngroup = self.group_info
        ids = ensure_platform_int(ids)
        if ngroup:
            out = np.bincount(ids[ids != -1], minlength=ngroup)
        else:
            out = []
        return Series(out, index=self.result_index, dtype="int64")
