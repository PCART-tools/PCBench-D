    def slice_indexer(self, start=None, end=None, step=None, kind=lib.no_default):
        """
        Return indexer for specified label slice.
        Index.slice_indexer, customized to handle time slicing.

        In addition to functionality provided by Index.slice_indexer, does the
        following:

        - if both `start` and `end` are instances of `datetime.time`, it
          invokes `indexer_between_time`
        - if `start` and `end` are both either string or None perform
          value-based selection in non-monotonic cases.

        """
        self._deprecated_arg(kind, "kind", "slice_indexer")

        # For historical reasons DatetimeIndex supports slices between two
        # instances of datetime.time as if it were applying a slice mask to
        # an array of (self.hour, self.minute, self.seconds, self.microsecond).
        if isinstance(start, time) and isinstance(end, time):
            if step is not None and step != 1:
                raise ValueError("Must have step size of 1 with time slices")
            return self.indexer_between_time(start, end)

        if isinstance(start, time) or isinstance(end, time):
            raise KeyError("Cannot mix time and non-time slice keys")

        def check_str_or_none(point):
            return point is not None and not isinstance(point, str)

        # GH#33146 if start and end are combinations of str and None and Index is not
        # monotonic, we can not use Index.slice_indexer because it does not honor the
        # actual elements, is only searching for start and end
        if (
            check_str_or_none(start)
            or check_str_or_none(end)
            or self.is_monotonic_increasing
        ):
            return Index.slice_indexer(self, start, end, step, kind=kind)

        mask = np.array(True)
        deprecation_mask = np.array(True)
        if start is not None:
            start_casted = self._maybe_cast_slice_bound(start, "left")
            mask = start_casted <= self
            deprecation_mask = start_casted == self

        if end is not None:
            end_casted = self._maybe_cast_slice_bound(end, "right")
            mask = (self <= end_casted) & mask
            deprecation_mask = (end_casted == self) | deprecation_mask

        if not deprecation_mask.any():
            warnings.warn(
                "Value based partial slicing on non-monotonic DatetimeIndexes "
                "with non-existing keys is deprecated and will raise a "
                "KeyError in a future Version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        indexer = mask.nonzero()[0][::step]
        if len(indexer) == len(self):
            return slice(None)
        else:
            return indexer
