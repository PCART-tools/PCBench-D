    @deprecate_renamed_function("rolling", version="0.19.0")
    def groupby_rolling(
        self,
        index_column: IntoExpr,
        *,
        period: str | timedelta,
        offset: str | timedelta | None = None,
        closed: ClosedInterval = "right",
        by: IntoExpr | Iterable[IntoExpr] | None = None,
        check_sorted: bool = True,
    ) -> RollingGroupBy:
        """
        Create rolling groups based on a time, Int32, or Int64 column.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`DataFrame.rolling`.

        Parameters
        ----------
        index_column
            Column used to group based on the time window.
            Often of type Date/Datetime.
            This column must be sorted in ascending order (or, if `by` is specified,
            then it must be sorted in ascending order within each group).

            In case of a rolling group by on indices, dtype needs to be one of
            {Int32, Int64}. Note that Int32 gets temporarily cast to Int64, so if
            performance matters use an Int64 column.
        period
            length of the window - must be non-negative
        offset
            offset of the window. Default is -period
        closed : {'right', 'left', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive).
        by
            Also group by this column/these columns
        check_sorted
            When the `by` argument is given, polars can not check sortedness
            by the metadata and has to do a full scan on the index column to
            verify data is sorted. This is expensive. If you are sure the
            data within the by groups is sorted, you can set this to `False`.
            Doing so incorrectly will lead to incorrect output

        """
        return self.rolling(
            index_column,
            period=period,
            offset=offset,
            closed=closed,
            by=by,
            check_sorted=check_sorted,
        )
