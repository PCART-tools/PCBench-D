    def _set_axis(self, axis: int, labels: AnyArrayLike | list) -> None:
        """
        Override generic, we want to set the _typ here.

        This is called from the cython code when we set the `index` attribute
        directly, e.g. `series.index = [1, 2, 3]`.
        """
        labels = ensure_index(labels)

        if labels._is_all_dates and not (
            type(labels) is Index and not isinstance(labels.dtype, np.dtype)
        ):
            # exclude e.g. timestamp[ns][pyarrow] dtype from this casting
            deep_labels = labels
            if isinstance(labels, CategoricalIndex):
                deep_labels = labels.categories

            if not isinstance(
                deep_labels, (DatetimeIndex, PeriodIndex, TimedeltaIndex)
            ):
                try:
                    labels = DatetimeIndex(labels)
                except (tslibs.OutOfBoundsDatetime, ValueError):
                    # labels may exceeds datetime bounds,
                    # or not be a DatetimeIndex
                    pass

        # The ensure_index call above ensures we have an Index object
        self._mgr.set_axis(axis, labels)
