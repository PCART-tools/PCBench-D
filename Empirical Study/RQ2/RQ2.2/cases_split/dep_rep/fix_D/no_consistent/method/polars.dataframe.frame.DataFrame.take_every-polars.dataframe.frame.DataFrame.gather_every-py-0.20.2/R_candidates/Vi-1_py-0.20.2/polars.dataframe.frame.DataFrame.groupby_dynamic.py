    @deprecate_renamed_function("group_by_dynamic", version="0.19.0")
    def groupby_dynamic(
        self,
        index_column: IntoExpr,
        *,
        every: str | timedelta,
        period: str | timedelta | None = None,
        offset: str | timedelta | None = None,
        truncate: bool = True,
        include_boundaries: bool = False,
        closed: ClosedInterval = "left",
        by: IntoExpr | Iterable[IntoExpr] | None = None,
        start_by: StartBy = "window",
        check_sorted: bool = True,
    ) -> DynamicGroupBy:
        """
        Group based on a time value (or index value of type Int32, Int64).

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`DataFrame.group_by_dynamic`.

        Parameters
        ----------
        index_column
            Column used to group based on the time window.
            Often of type Date/Datetime.
            This column must be sorted in ascending order (or, if `by` is specified,
            then it must be sorted in ascending order within each group).

            In case of a dynamic group by on indices, dtype needs to be one of
            {Int32, Int64}. Note that Int32 gets temporarily cast to Int64, so if
            performance matters use an Int64 column.
        every
            interval of the window
        period
            length of the window, if None it will equal 'every'
        offset
            offset of the window, only takes effect if `start_by` is `'window'`.
            Defaults to negative `every`.
        truncate
            truncate the time value to the window lower bound
        include_boundaries
            Add the lower and upper bound of the window to the "_lower_bound" and
            "_upper_bound" columns. This will impact performance because it's harder to
            parallelize
        closed : {'left', 'right', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive).
        by
            Also group by this column/these columns
        start_by : {'window', 'datapoint', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
            The strategy to determine the start of the first window by.

            * 'window': Start by taking the earliest timestamp, truncating it with
              `every`, and then adding `offset`.
              Note that weekly windows start on Monday.
            * 'datapoint': Start from the first encountered data point.
            * a day of the week (only takes effect if `every` contains `'w'`):

              * 'monday': Start the window on the Monday before the first data point.
              * 'tuesday': Start the window on the Tuesday before the first data point.
              * ...
              * 'sunday': Start the window on the Sunday before the first data point.
        check_sorted
            When the `by` argument is given, polars can not check sortedness
            by the metadata and has to do a full scan on the index column to
            verify data is sorted. This is expensive. If you are sure the
            data within the by groups is sorted, you can set this to `False`.
            Doing so incorrectly will lead to incorrect output

        Returns
        -------
        DynamicGroupBy
            Object you can call `.agg` on to aggregate by groups, the result
            of which will be sorted by `index_column` (but note that if `by` columns are
            passed, it will only be sorted within each `by` group).

        """  # noqa: W505
        return self.group_by_dynamic(
            index_column,
            every=every,
            period=period,
            offset=offset,
            truncate=truncate,
            include_boundaries=include_boundaries,
            closed=closed,
            by=by,
            start_by=start_by,
            check_sorted=check_sorted,
        )
