    def slice_indexer(self, start=None, end=None, step=None):
        """
        For an ordered Index, compute the slice indexer for input labels and
        step

        Parameters
        ----------
        start : label, default None
            If None, defaults to the beginning
        end : label, default None
            If None, defaults to the end
        step : int, default None

        Returns
        -------
        indexer : ndarray or slice

        Notes
        -----
        This function assumes that the data is sorted, so use at your own peril
        """
        start_slice, end_slice = self.slice_locs(start, end)

        # return a slice
        if np.isscalar(start_slice) and np.isscalar(end_slice):

            # degenerate cases
            if start is None and end is None:
                return slice(None, None, step)

            return slice(start_slice, end_slice, step)

        # loc indexers
        return Index(start_slice) & Index(end_slice)
