    def _convert_slice_indexer(self, key: slice, kind: Literal["loc", "getitem"]):
        """
        Convert a slice indexer.

        By definition, these are labels unless 'iloc' is passed in.
        Floats are not allowed as the start, step, or stop of the slice.

        Parameters
        ----------
        key : label of the slice bound
        kind : {'loc', 'getitem'}
        """

        # potentially cast the bounds to integers
        start, stop, step = key.start, key.stop, key.step

        # figure out if this is a positional indexer
        is_index_slice = is_valid_positional_slice(key)

        # TODO(GH#50617): once Series.__[gs]etitem__ is removed we should be able
        #  to simplify this.
        if lib.is_np_dtype(self.dtype, "f"):
            # We always treat __getitem__ slicing as label-based
            # translate to locations
            if kind == "getitem" and is_index_slice and not start == stop and step != 0:
                # exclude step=0 from the warning because it will raise anyway
                # start/stop both None e.g. [:] or [::-1] won't change.
                # exclude start==stop since it will be empty either way, or
                # will be [:] or [::-1] which won't change
                warnings.warn(
                    # GH#49612
                    "The behavior of obj[i:j] with a float-dtype index is "
                    "deprecated. In a future version, this will be treated as "
                    "positional instead of label-based. For label-based slicing, "
                    "use obj.loc[i:j] instead",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            return self.slice_indexer(start, stop, step)

        if kind == "getitem":
            # called from the getitem slicers, validate that we are in fact integers
            if is_index_slice:
                # In this case the _validate_indexer checks below are redundant
                return key
            elif self.dtype.kind in "iu":
                # Note: these checks are redundant if we know is_index_slice
                self._validate_indexer("slice", key.start, "getitem")
                self._validate_indexer("slice", key.stop, "getitem")
                self._validate_indexer("slice", key.step, "getitem")
                return key

        # convert the slice to an indexer here

        # special case for interval_dtype bc we do not do partial-indexing
        #  on integer Intervals when slicing
        # TODO: write this in terms of e.g. should_partial_index?
        ints_are_positional = self._should_fallback_to_positional or isinstance(
            self.dtype, IntervalDtype
        )
        is_positional = is_index_slice and ints_are_positional

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
                raise TypeError(
                    "Slicing a positional slice with .loc is not allowed, "
                    "Use .loc with labels or .iloc with positions instead.",
                )
            indexer = key
        else:
            indexer = self.slice_indexer(start, stop, step)

        return indexer
