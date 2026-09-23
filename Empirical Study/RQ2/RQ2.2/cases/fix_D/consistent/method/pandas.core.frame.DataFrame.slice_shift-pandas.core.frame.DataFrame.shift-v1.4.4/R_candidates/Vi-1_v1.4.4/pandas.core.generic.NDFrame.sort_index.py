    def sort_index(
        self,
        axis=0,
        level=None,
        ascending: bool_t | int | Sequence[bool_t | int] = True,
        inplace: bool_t = False,
        kind: str = "quicksort",
        na_position: str = "last",
        sort_remaining: bool_t = True,
        ignore_index: bool_t = False,
        key: IndexKeyFunc = None,
    ):

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
                result = self.copy()

            if ignore_index:
                result.index = default_index(len(self))
            if inplace:
                return
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
