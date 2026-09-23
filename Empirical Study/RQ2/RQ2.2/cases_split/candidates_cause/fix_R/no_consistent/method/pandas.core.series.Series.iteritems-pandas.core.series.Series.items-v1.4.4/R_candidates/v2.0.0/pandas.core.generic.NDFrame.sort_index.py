    def sort_index(
        self: NDFrameT,
        *,
        axis: Axis = 0,
        level: IndexLabel = None,
        ascending: bool_t | Sequence[bool_t] = True,
        inplace: bool_t = False,
        kind: SortKind = "quicksort",
        na_position: NaPosition = "last",
        sort_remaining: bool_t = True,
        ignore_index: bool_t = False,
        key: IndexKeyFunc = None,
    ) -> NDFrameT | None:
        inplace = validate_bool_kwarg(inplace, "inplace")
        axis = self._get_axis_number(axis)
        ascending = validate_ascending(ascending)

        target = self._get_axis(axis)

        indexer = get_indexer_indexer(
            target, level, ascending, kind, na_position, sort_remaining, key
        )

        if indexer is None:
            if inplace:
                result = self
            else:
                result = self.copy(deep=None)

            if ignore_index:
                result.index = default_index(len(self))
            if inplace:
                return None
            else:
                return result

        baxis = self._get_block_manager_axis(axis)
        new_data = self._mgr.take(indexer, axis=baxis, verify=False)

        # reconstruct axis if needed
        new_data.set_axis(baxis, new_data.axes[baxis]._sort_levels_monotonic())

        if ignore_index:
            axis = 1 if isinstance(self, ABCDataFrame) else 0
            new_data.set_axis(axis, default_index(len(indexer)))

        result = self._constructor(new_data)

        if inplace:
            return self._update_inplace(result)
        else:
            return result.__finalize__(self, method="sort_index")
