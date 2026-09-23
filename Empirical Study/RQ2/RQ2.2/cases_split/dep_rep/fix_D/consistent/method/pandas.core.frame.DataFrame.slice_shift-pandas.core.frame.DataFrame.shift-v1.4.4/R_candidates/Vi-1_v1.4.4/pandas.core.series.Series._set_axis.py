    def _set_axis(self, axis: int, labels, fastpath: bool = False) -> None:
        """
        Override generic, we want to set the _typ here.

        This is called from the cython code when we set the `index` attribute
        directly, e.g. `series.index = [1, 2, 3]`.
        """
        if not fastpath:
            labels = ensure_index(labels)

        if labels._is_all_dates:
            deep_labels = labels
            if isinstance(labels, CategoricalIndex):
                deep_labels = labels.categories

            if not isinstance(
                deep_labels, (DatetimeIndex, PeriodIndex, TimedeltaIndex)
            ):
                try:
                    labels = DatetimeIndex(labels)
                    # need to set here because we changed the index
                    if fastpath:
                        self._mgr.set_axis(axis, labels)
                except (tslibs.OutOfBoundsDatetime, ValueError):
                    # labels may exceeds datetime bounds,
                    # or not be a DatetimeIndex
                    pass

        if not fastpath:
            # The ensure_index call above ensures we have an Index object
            self._mgr.set_axis(axis, labels)
