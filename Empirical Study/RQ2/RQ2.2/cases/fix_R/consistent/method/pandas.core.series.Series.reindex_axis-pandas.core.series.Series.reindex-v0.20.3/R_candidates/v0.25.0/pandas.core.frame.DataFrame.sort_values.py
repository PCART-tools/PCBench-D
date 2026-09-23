    @Substitution(**_shared_doc_kwargs)
    @Appender(NDFrame.sort_values.__doc__)
    def sort_values(
        self,
        by,
        axis=0,
        ascending=True,
        inplace=False,
        kind="quicksort",
        na_position="last",
    ):
        inplace = validate_bool_kwarg(inplace, "inplace")
        axis = self._get_axis_number(axis)

        if not isinstance(by, list):
            by = [by]
        if is_sequence(ascending) and len(by) != len(ascending):
            raise ValueError(
                "Length of ascending (%d) != length of by (%d)"
                % (len(ascending), len(by))
            )
        if len(by) > 1:
            from pandas.core.sorting import lexsort_indexer

            keys = [self._get_label_or_level_values(x, axis=axis) for x in by]
            indexer = lexsort_indexer(keys, orders=ascending, na_position=na_position)
            indexer = ensure_platform_int(indexer)
        else:
            from pandas.core.sorting import nargsort

            by = by[0]
            k = self._get_label_or_level_values(by, axis=axis)

            if isinstance(ascending, (tuple, list)):
                ascending = ascending[0]

            indexer = nargsort(
                k, kind=kind, ascending=ascending, na_position=na_position
            )

        new_data = self._data.take(
            indexer, axis=self._get_block_manager_axis(axis), verify=False
        )

        if inplace:
            return self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
