    @final
    def _align_frame(
        self,
        other: DataFrame,
        join: AlignJoin = "outer",
        axis: Axis | None = None,
        level=None,
        copy: bool_t | None = None,
        fill_value=None,
        method=None,
        limit: int | None = None,
        fill_axis: Axis = 0,
    ) -> tuple[Self, DataFrame, Index | None]:
        # defaults
        join_index, join_columns = None, None
        ilidx, iridx = None, None
        clidx, cridx = None, None

        is_series = isinstance(self, ABCSeries)

        if (axis is None or axis == 0) and not self.index.equals(other.index):
            join_index, ilidx, iridx = self.index.join(
                other.index, how=join, level=level, return_indexers=True
            )

        if (
            (axis is None or axis == 1)
            and not is_series
            and not self.columns.equals(other.columns)
        ):
            join_columns, clidx, cridx = self.columns.join(
                other.columns, how=join, level=level, return_indexers=True
            )

        if is_series:
            reindexers = {0: [join_index, ilidx]}
        else:
            reindexers = {0: [join_index, ilidx], 1: [join_columns, clidx]}

        left = self._reindex_with_indexers(
            reindexers, copy=copy, fill_value=fill_value, allow_dups=True
        )
        # other must be always DataFrame
        right = other._reindex_with_indexers(
            {0: [join_index, iridx], 1: [join_columns, cridx]},
            copy=copy,
            fill_value=fill_value,
            allow_dups=True,
        )

        if method is not None:
            left = left._pad_or_backfill(method, axis=fill_axis, limit=limit)
            right = right._pad_or_backfill(method, axis=fill_axis, limit=limit)

        return left, right, join_index
