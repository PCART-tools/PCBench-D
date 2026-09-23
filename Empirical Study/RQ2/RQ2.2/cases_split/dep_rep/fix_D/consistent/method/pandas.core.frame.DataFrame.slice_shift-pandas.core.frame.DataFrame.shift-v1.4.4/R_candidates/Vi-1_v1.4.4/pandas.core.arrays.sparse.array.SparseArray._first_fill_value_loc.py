    def _first_fill_value_loc(self):
        """
        Get the location of the first missing value.

        Returns
        -------
        int
        """
        if len(self) == 0 or self.sp_index.npoints == len(self):
            return -1

        indices = self.sp_index.indices
        if not len(indices) or indices[0] > 0:
            return 0

        diff = indices[1:] - indices[:-1]
        return np.searchsorted(diff, 2) + 1
