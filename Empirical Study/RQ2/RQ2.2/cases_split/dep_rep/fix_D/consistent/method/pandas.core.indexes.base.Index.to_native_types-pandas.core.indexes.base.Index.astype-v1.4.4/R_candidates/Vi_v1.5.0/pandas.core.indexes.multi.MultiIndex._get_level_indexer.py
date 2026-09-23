    def _get_level_indexer(
        self, key, level: int = 0, indexer: npt.NDArray[np.bool_] | None = None
    ):
        # `level` kwarg is _always_ positional, never name
        # return a boolean array or slice showing where the key is
        # in the totality of values
        # if the indexer is provided, then use this

        level_index = self.levels[level]
        level_codes = self.codes[level]

        def convert_indexer(start, stop, step, indexer=indexer, codes=level_codes):
            # Compute a bool indexer to identify the positions to take.
            # If we have an existing indexer, we only need to examine the
            # subset of positions where the existing indexer is True.
            if indexer is not None:
                # we only need to look at the subset of codes where the
                # existing indexer equals True
                codes = codes[indexer]

            if step is None or step == 1:
                new_indexer = (codes >= start) & (codes < stop)
            else:
                r = np.arange(start, stop, step, dtype=codes.dtype)
                new_indexer = algos.isin(codes, r)

            if indexer is None:
                return new_indexer

            indexer = indexer.copy()
            indexer[indexer] = new_indexer
            return indexer

        if isinstance(key, slice):
            # handle a slice, returning a slice if we can
            # otherwise a boolean indexer
            step = key.step
            is_negative_step = step is not None and step < 0

            try:
                if key.start is not None:
                    start = level_index.get_loc(key.start)
                elif is_negative_step:
                    start = len(level_index) - 1
                else:
                    start = 0

                if key.stop is not None:
                    stop = level_index.get_loc(key.stop)
                elif is_negative_step:
                    stop = 0
                elif isinstance(start, slice):
                    stop = len(level_index)
                else:
                    stop = len(level_index) - 1
            except KeyError:

                # we have a partial slice (like looking up a partial date
                # string)
                start = stop = level_index.slice_indexer(key.start, key.stop, key.step)
                step = start.step

            if isinstance(start, slice) or isinstance(stop, slice):
                # we have a slice for start and/or stop
                # a partial date slicer on a DatetimeIndex generates a slice
                # note that the stop ALREADY includes the stopped point (if
                # it was a string sliced)
                start = getattr(start, "start", start)
                stop = getattr(stop, "stop", stop)
                return convert_indexer(start, stop, step)

            elif level > 0 or self._lexsort_depth == 0 or step is not None:
                # need to have like semantics here to right
                # searching as when we are using a slice
                # so adjust the stop by 1 (so we include stop)
                stop = (stop - 1) if is_negative_step else (stop + 1)
                return convert_indexer(start, stop, step)
            else:
                # sorted, so can return slice object -> view
                i = algos.searchsorted(level_codes, start, side="left")
                j = algos.searchsorted(level_codes, stop, side="right")
                return slice(i, j, step)

        else:

            idx = self._get_loc_single_level_index(level_index, key)

            if level > 0 or self._lexsort_depth == 0:
                # Desired level is not sorted
                if isinstance(idx, slice):
                    # test_get_loc_partial_timestamp_multiindex
                    locs = (level_codes >= idx.start) & (level_codes < idx.stop)
                    return locs

                locs = np.array(level_codes == idx, dtype=bool, copy=False)

                if not locs.any():
                    # The label is present in self.levels[level] but unused:
                    raise KeyError(key)
                return locs

            if isinstance(idx, slice):
                # e.g. test_partial_string_timestamp_multiindex
                start = algos.searchsorted(level_codes, idx.start, side="left")
                # NB: "left" here bc of slice semantics
                end = algos.searchsorted(level_codes, idx.stop, side="left")
            else:
                start = algos.searchsorted(level_codes, idx, side="left")
                end = algos.searchsorted(level_codes, idx, side="right")

            if start == end:
                # The label is present in self.levels[level] but unused:
                raise KeyError(key)
            return slice(start, end)
