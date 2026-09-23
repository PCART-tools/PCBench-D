    def _partial_tup_index(self, tup: tuple, side: Literal["left", "right"] = "left"):
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
                    loc = algos.searchsorted(lev, lab, side=side)
                except TypeError as err:
                    # non-comparable e.g. test_slice_locs_with_type_mismatch
                    raise TypeError(f"Level type mismatch: {lab}") from err
                if not is_integer(loc):
                    # non-comparable level, e.g. test_groupby_example
                    raise TypeError(f"Level type mismatch: {lab}")
                if side == "right" and loc >= 0:
                    loc -= 1
                return start + algos.searchsorted(section, loc, side=side)

            idx = self._get_loc_single_level_index(lev, lab)
            if isinstance(idx, slice) and k < n - 1:
                # Get start and end value from slice, necessary when a non-integer
                # interval is given as input GH#37707
                start = idx.start
                end = idx.stop
            elif k < n - 1:
                # error: Incompatible types in assignment (expression has type
                # "Union[ndarray[Any, dtype[signedinteger[Any]]]
                end = start + algos.searchsorted(  # type: ignore[assignment]
                    section, idx, side="right"
                )
                # error: Incompatible types in assignment (expression has type
                # "Union[ndarray[Any, dtype[signedinteger[Any]]]
                start = start + algos.searchsorted(  # type: ignore[assignment]
                    section, idx, side="left"
                )
            elif isinstance(idx, slice):
                idx = idx.start
                return start + algos.searchsorted(section, idx, side=side)
            else:
                return start + algos.searchsorted(section, idx, side=side)
