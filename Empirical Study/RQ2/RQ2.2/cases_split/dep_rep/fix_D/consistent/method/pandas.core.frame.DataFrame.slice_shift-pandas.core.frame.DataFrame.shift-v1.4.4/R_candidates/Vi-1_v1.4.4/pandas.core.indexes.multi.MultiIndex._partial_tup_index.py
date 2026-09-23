    def _partial_tup_index(self, tup: tuple, side="left"):
        if len(tup) > self._lexsort_depth:
            raise UnsortedIndexError(
                f"Key length ({len(tup)}) was greater than MultiIndex lexsort depth "
                f"({self._lexsort_depth})"
            )

        n = len(tup)
        start, end = 0, len(self)
        zipped = zip(tup, self.levels, self.codes)
        for k, (lab, lev, level_codes) in enumerate(zipped):
            section = level_codes[start:end]

            if lab not in lev and not isna(lab):
                # short circuit
                try:
                    loc = lev.searchsorted(lab, side=side)
                except TypeError as err:
                    # non-comparable e.g. test_slice_locs_with_type_mismatch
                    raise TypeError(f"Level type mismatch: {lab}") from err
                if not is_integer(loc):
                    # non-comparable level, e.g. test_groupby_example
                    raise TypeError(f"Level type mismatch: {lab}")
                if side == "right" and loc >= 0:
                    loc -= 1
                return start + section.searchsorted(loc, side=side)

            idx = self._get_loc_single_level_index(lev, lab)
            if isinstance(idx, slice) and k < n - 1:
                # Get start and end value from slice, necessary when a non-integer
                # interval is given as input GH#37707
                start = idx.start
                end = idx.stop
            elif k < n - 1:
                end = start + section.searchsorted(idx, side="right")
                start = start + section.searchsorted(idx, side="left")
            elif isinstance(idx, slice):
                idx = idx.start
                return start + section.searchsorted(idx, side=side)
            else:
                return start + section.searchsorted(idx, side=side)
