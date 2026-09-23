    @deprecate_nonkeyword_arguments(["self", "breaks"], version="0.19.0")
    @deprecate_renamed_parameter("series", "as_series", version="0.19.0")
    @unstable()
    def cut(
        self,
        breaks: Sequence[float],
        labels: Sequence[str] | None = None,
        break_point_label: str = "break_point",
        category_label: str = "category",
        *,
        left_closed: bool = False,
        include_breaks: bool = False,
        as_series: bool = True,
    ) -> Series | DataFrame:
        """
        Bin continuous values into discrete categories.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        breaks
            List of unique cut points.
        labels
            Names of the categories. The number of labels must be equal to the number
            of cut points plus one.
        break_point_label
            Name of the breakpoint column. Only used if `include_breaks` is set to
            `True`.

            .. deprecated:: 0.19.0
                This parameter will be removed. Use `Series.struct.rename_fields` to
                rename the field instead.
        category_label
            Name of the category column. Only used if `include_breaks` is set to
            `True`.

            .. deprecated:: 0.19.0
                This parameter will be removed. Use `Series.struct.rename_fields` to
                rename the field instead.
        left_closed
            Set the intervals to be left-closed instead of right-closed.
        include_breaks
            Include a column with the right endpoint of the bin each observation falls
            in. This will change the data type of the output from a
            :class:`Categorical` to a :class:`Struct`.
        as_series
            If set to `False`, return a DataFrame containing the original values,
            the breakpoints, and the categories.

            .. deprecated:: 0.19.0
                This parameter will be removed. The same behavior can be achieved by
                setting `include_breaks=True`, unnesting the resulting struct Series,
                and adding the result to the original Series.

        Returns
        -------
        Series
            Series of data type :class:`Categorical` if `include_breaks` is set to
            `False` (default), otherwise a Series of data type :class:`Struct`.

        See Also
        --------
        qcut

        Examples
        --------
        Divide the column into three categories.

        >>> s = pl.Series("foo", [-2, -1, 0, 1, 2])
        >>> s.cut([-1, 1], labels=["a", "b", "c"])
        shape: (5,)
        Series: 'foo' [cat]
        [
                "a"
                "a"
                "b"
                "b"
                "c"
        ]

        Create a DataFrame with the breakpoint and category for each value.

        >>> cut = s.cut([-1, 1], include_breaks=True).alias("cut")
        >>> s.to_frame().with_columns(cut).unnest("cut")
        shape: (5, 3)
        ┌─────┬─────────────┬────────────┐
        │ foo ┆ break_point ┆ category   │
        │ --- ┆ ---         ┆ ---        │
        │ i64 ┆ f64         ┆ cat        │
        ╞═════╪═════════════╪════════════╡
        │ -2  ┆ -1.0        ┆ (-inf, -1] │
        │ -1  ┆ -1.0        ┆ (-inf, -1] │
        │ 0   ┆ 1.0         ┆ (-1, 1]    │
        │ 1   ┆ 1.0         ┆ (-1, 1]    │
        │ 2   ┆ inf         ┆ (1, inf]   │
        └─────┴─────────────┴────────────┘
        """
        if break_point_label != "break_point":
            issue_deprecation_warning(
                "The `break_point_label` parameter for `Series.cut` will be removed."
                " Use `Series.struct.rename_fields` to rename the field instead.",
                version="0.19.0",
            )
        if category_label != "category":
            issue_deprecation_warning(
                "The `category_label` parameter for `Series.cut` will be removed."
                " Use `Series.struct.rename_fields` to rename the field instead.",
                version="0.19.0",
            )
        if not as_series:
            issue_deprecation_warning(
                "The `as_series` parameter for `Series.cut` will be removed."
                " The same behavior can be achieved by setting `include_breaks=True`,"
                " unnesting the resulting struct Series,"
                " and adding the result to the original Series.",
                version="0.19.0",
            )
            temp_name = self.name + "_bin"
            return (
                self.to_frame()
                .with_columns(
                    F.col(self.name)
                    .cut(
                        breaks,
                        labels=labels,
                        left_closed=left_closed,
                        include_breaks=True,  # always include breaks
                    )
                    .alias(temp_name)
                )
                .unnest(temp_name)
                .rename({"brk": break_point_label, temp_name: category_label})
            )

        result = (
            self.to_frame()
            .select_seq(
                F.col(self.name).cut(
                    breaks,
                    labels=labels,
                    left_closed=left_closed,
                    include_breaks=include_breaks,
                )
            )
            .to_series()
        )

        if include_breaks:
            result = result.struct.rename_fields([break_point_label, category_label])

        return result
