    def get_slice_bound(self, label, side, kind):
        """
        Calculate slice bound that corresponds to given label.

        Returns leftmost (one-past-the-rightmost if ``side=='right'``) position
        of given label.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'ix', 'loc', 'getitem'}

        """
        assert kind in ['ix', 'loc', 'getitem', None]

        if side not in ('left', 'right'):
            raise ValueError("Invalid value for side kwarg,"
                             " must be either 'left' or 'right': %s" %
                             (side, ))

        original_label = label

        # For datetime indices label may be a string that has to be converted
        # to datetime boundary according to its resolution.
        label = self._maybe_cast_slice_bound(label, side, kind)

        # we need to look up the label
        try:
            slc = self._get_loc_only_exact_matches(label)
        except KeyError as err:
            try:
                return self._searchsorted_monotonic(label, side)
            except ValueError:
                # raise the original KeyError
                raise err

        if isinstance(slc, np.ndarray):
            # get_loc may return a boolean array or an array of indices, which
            # is OK as long as they are representable by a slice.
            if is_bool_dtype(slc):
                slc = lib.maybe_booleans_to_slice(slc.view('u1'))
            else:
                slc = lib.maybe_indices_to_slice(slc.astype('i8'), len(self))
            if isinstance(slc, np.ndarray):
                raise KeyError("Cannot get %s slice bound for non-unique "
                               "label: %r" % (side, original_label))

        if isinstance(slc, slice):
            if side == 'left':
                return slc.start
            else:
                return slc.stop
        else:
            if side == 'right':
                return slc + 1
            else:
                return slc
