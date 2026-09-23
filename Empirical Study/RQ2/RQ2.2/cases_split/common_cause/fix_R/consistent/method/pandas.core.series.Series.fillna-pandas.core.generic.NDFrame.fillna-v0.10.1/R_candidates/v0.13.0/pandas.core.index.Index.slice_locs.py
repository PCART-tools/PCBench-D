    def slice_locs(self, start=None, end=None):
        """
        For an ordered Index, compute the slice locations for input labels

        Parameters
        ----------
        start : label, default None
            If None, defaults to the beginning
        end : label, default None
            If None, defaults to the end

        Returns
        -------
        (start, end) : (int, int)

        Notes
        -----
        This function assumes that the data is sorted, so use at your own peril
        """

        is_unique = self.is_unique
        if start is None:
            start_slice = 0
        else:
            try:
                start_slice = self.get_loc(start)

                if not is_unique:

                    # get_loc will return a boolean array for non_uniques
                    # if we are not monotonic
                    if isinstance(start_slice, np.ndarray):
                        raise KeyError("cannot peform a slice operation "
                                       "on a non-unique non-monotonic index")

                if isinstance(start_slice, slice):
                    start_slice = start_slice.start

            except KeyError:
                if self.is_monotonic:
                    start_slice = self.searchsorted(start, side='left')
                else:
                    raise

        if end is None:
            end_slice = len(self)
        else:
            try:
                end_slice = self.get_loc(end)

                if not is_unique:

                    # get_loc will return a boolean array for non_uniques
                    if isinstance(end_slice, np.ndarray):
                        raise KeyError("cannot perform a slice operation "
                                       "on a non-unique non-monotonic index")

                if isinstance(end_slice, slice):
                    end_slice = end_slice.stop
                else:
                    end_slice += 1

            except KeyError:
                if self.is_monotonic:
                    end_slice = self.searchsorted(end, side='right')
                else:
                    raise

        return start_slice, end_slice
