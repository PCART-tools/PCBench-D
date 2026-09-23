    def get_loc(self, key, method=None):
        """
        Get location for a label or a tuple of labels.

        The location is returned as an integer/slice or boolean
        mask.

        Parameters
        ----------
        key : label or tuple of labels (one for each level)
        method : None

        Returns
        -------
        loc : int, slice object or boolean mask
            If the key is past the lexsort depth, the return may be a
            boolean mask array, otherwise it is always a slice or int.

        See Also
        --------
        Index.get_loc : The get_loc method for (single-level) index.
        MultiIndex.slice_locs : Get slice location given start label(s) and
                                end label(s).
        MultiIndex.get_locs : Get location for a label/slice/list/mask or a
                              sequence of such.

        Notes
        -----
        The key cannot be a slice, list of same-level labels, a boolean mask,
        or a sequence of such. If you want to use those, use
        :meth:`MultiIndex.get_locs` instead.

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([list('abb'), list('def')])

        >>> mi.get_loc('b')
        slice(1, 3, None)

        >>> mi.get_loc(('b', 'e'))
        1
        """
        if method is not None:
            raise NotImplementedError(
                "only the default get_loc method is "
                "currently supported for MultiIndex"
            )

        self._check_indexing_error(key)

        def _maybe_to_slice(loc):
            """convert integer indexer to boolean mask or slice if possible"""
            if not isinstance(loc, np.ndarray) or loc.dtype != np.intp:
                return loc

            loc = lib.maybe_indices_to_slice(loc, len(self))
            if isinstance(loc, slice):
                return loc

            mask = np.empty(len(self), dtype="bool")
            mask.fill(False)
            mask[loc] = True
            return mask

        if not isinstance(key, tuple):
            loc = self._get_level_indexer(key, level=0)
            return _maybe_to_slice(loc)

        keylen = len(key)
        if self.nlevels < keylen:
            raise KeyError(
                f"Key length ({keylen}) exceeds index depth ({self.nlevels})"
            )

        if keylen == self.nlevels and self.is_unique:
            try:
                return self._engine.get_loc(key)
            except TypeError:
                # e.g. test_partial_slicing_with_multiindex partial string slicing
                loc, _ = self.get_loc_level(key, list(range(self.nlevels)))
                return loc

        # -- partial selection or non-unique index
        # break the key into 2 parts based on the lexsort_depth of the index;
        # the first part returns a continuous slice of the index; the 2nd part
        # needs linear search within the slice
        i = self._lexsort_depth
        lead_key, follow_key = key[:i], key[i:]

        if not lead_key:
            start = 0
            stop = len(self)
        else:
            try:
                start, stop = self.slice_locs(lead_key, lead_key)
            except TypeError as err:
                # e.g. test_groupby_example key = ((0, 0, 1, 2), "new_col")
                #  when self has 5 integer levels
                raise KeyError(key) from err

        if start == stop:
            raise KeyError(key)

        if not follow_key:
            return slice(start, stop)

        warnings.warn(
            "indexing past lexsort depth may impact performance.",
            PerformanceWarning,
            stacklevel=find_stack_level(),
        )

        loc = np.arange(start, stop, dtype=np.intp)

        for i, k in enumerate(follow_key, len(lead_key)):
            mask = self.codes[i][loc] == self._get_loc_single_level_index(
                self.levels[i], k
            )
            if not mask.all():
                loc = loc[mask]
            if not len(loc):
                raise KeyError(key)

        return _maybe_to_slice(loc) if len(loc) != stop - start else slice(start, stop)
