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

        def _get_slice(starting_value, offset, search_side, slice_property,
                       search_value):
            if search_value is None:
                return starting_value

            try:
                slc = self.get_loc(search_value)

                if not is_unique:

                    # get_loc will return a boolean array for non_uniques
                    # if we are not monotonic
                    if isinstance(slc, (np.ndarray, Index)):
                        raise KeyError("cannot peform a slice operation "
                                       "on a non-unique non-monotonic index")

                if isinstance(slc, slice):
                    slc = getattr(slc, slice_property)
                else:
                    slc += offset

            except KeyError:
                if self.is_monotonic:

                    # we are duplicated but non-unique
                    # so if we have an indexer then we are done
                    # else search for it (GH 7523)
                    if not is_unique and is_integer(search_value):
                        slc = search_value
                    else:
                        slc = self.searchsorted(search_value,
                                                side=search_side)
                else:
                    raise
            return slc

        start_slice = _get_slice(0, offset=0, search_side='left',
                                 slice_property='start', search_value=start)
        end_slice = _get_slice(len(self), offset=1, search_side='right',
                               slice_property='stop', search_value=end)

        return start_slice, end_slice
