    def size(self):
        """
        Compute group sizes

        """
        # TODO: better impl
        labels, _, ngroups = self.group_info
        bin_counts = algos.value_counts(labels, sort=False)
        bin_counts = bin_counts.reindex(np.arange(ngroups))
        bin_counts.index = self.result_index
        return bin_counts
