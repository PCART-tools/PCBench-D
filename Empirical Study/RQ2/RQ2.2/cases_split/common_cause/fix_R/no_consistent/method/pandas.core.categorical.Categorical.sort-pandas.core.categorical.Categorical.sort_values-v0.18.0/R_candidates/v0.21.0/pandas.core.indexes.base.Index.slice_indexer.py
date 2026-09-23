    def slice_indexer(self, start=None, end=None, step=None, kind=None):
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
        kind : string, default None

        Returns
        -------
        indexer : ndarray or slice

        Notes
        -----
        This function assumes that the data is sorted, so use at your own peril
        """
        start_slice, end_slice = self.slice_locs(start, end, step=step,
                                                 kind=kind)

        # return a slice
        if not is_scalar(start_slice):
            raise AssertionError("Start slice bound is non-scalar")
        if not is_scalar(end_slice):
            raise AssertionError("End slice bound is non-scalar")

        return slice(start_slice, end_slice, step)
