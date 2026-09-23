    def _convert_slice_indexer(self, key: slice, kind: str_t, is_frame: bool = False):
        """
        Convert a slice indexer.

        By definition, these are labels unless 'iloc' is passed in.
        Floats are not allowed as the start, step, or stop of the slice.

        Parameters
        ----------
        key : label of the slice bound
        kind : {'loc', 'getitem'}
        is_frame : bool, default False
            Whether this is a slice called on DataFrame.__getitem__
            as opposed to Series.__getitem__
        """
        assert kind in ["loc", "getitem"], kind

        # potentially cast the bounds to integers
        start, stop, step = key.start, key.stop, key.step

        # figure out if this is a positional indexer
        def is_int(v):
            return v is None or is_integer(v)

        is_index_slice = is_int(start) and is_int(stop) and is_int(step)

        # special case for interval_dtype bc we do not do partial-indexing
        #  on integer Intervals when slicing
        # TODO: write this in terms of e.g. should_partial_index?
        ints_are_positional = self._should_fallback_to_positional or is_interval_dtype(
            self.dtype
        )
        is_positional = is_index_slice and ints_are_positional

        if kind == "getitem":
            """
            called from the getitem slicers, validate that we are in fact
            integers
            """
            if self.is_integer():
                if is_frame:
                    # unambiguously positional, no deprecation
                    pass
                elif start is None and stop is None:
                    # label-based vs positional is irrelevant
                    pass
                elif isinstance(self, ABCRangeIndex) and self._range == range(
                    len(self)
                ):
                    # In this case there is no difference between label-based
                    #  and positional, so nothing will change.
                    pass
                elif (
                    self.dtype.kind in ["i", "u"]
                    and self._is_strictly_monotonic_increasing
                    and len(self) > 0
                    and self[0] == 0
                    and self[-1] == len(self) - 1
                ):
                    # We are range-like, e.g. created with Index(np.arange(N))
                    pass
                elif not is_index_slice:
                    # we're going to raise, so don't bother warning, e.g.
                    #  test_integer_positional_indexing
                    pass
                else:
                    warnings.warn(
                        "The behavior of `series[i:j]` with an integer-dtype index "
                        "is deprecated. In a future version, this will be treated "
                        "as *label-based* indexing, consistent with e.g. `series[i]` "
                        "lookups. To retain the old behavior, use `series.iloc[i:j]`. "
                        "To get the future behavior, use `series.loc[i:j]`.",
                        FutureWarning,
                        stacklevel=find_stack_level(inspect.currentframe()),
                    )
            if self.is_integer() or is_index_slice:
                # Note: these checks are redundant if we know is_index_slice
                self._validate_indexer("slice", key.start, "getitem")
                self._validate_indexer("slice", key.stop, "getitem")
                self._validate_indexer("slice", key.step, "getitem")
                return key

        # convert the slice to an indexer here

        # if we are mixed and have integers
        if is_positional:
            try:
                # Validate start & stop
                if start is not None:
                    self.get_loc(start)
                if stop is not None:
                    self.get_loc(stop)
                is_positional = False
            except KeyError:
                pass

        if com.is_null_slice(key):
            # It doesn't matter if we are positional or label based
            indexer = key
        elif is_positional:
            if kind == "loc":
                # GH#16121, GH#24612, GH#31810
                warnings.warn(
                    "Slicing a positional slice with .loc is not supported, "
                    "and will raise TypeError in a future version.  "
                    "Use .loc with labels or .iloc with positions instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(inspect.currentframe()),
                )
            indexer = key
        else:
            indexer = self.slice_indexer(start, stop, step)

        return indexer
