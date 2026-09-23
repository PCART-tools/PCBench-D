    @deprecate_renamed_function("group_by", version="0.19.0")
    def groupby(
        self,
        by: IntoExpr | Iterable[IntoExpr],
        *more_by: IntoExpr,
        maintain_order: bool = False,
    ) -> GroupBy:
        """
        Start a group by operation.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`DataFrame.group_by`.

        Parameters
        ----------
        by
            Column(s) to group by. Accepts expression input. Strings are parsed as
            column names.
        *more_by
            Additional columns to group by, specified as positional arguments.
        maintain_order
            Ensure that the order of the groups is consistent with the input data.
            This is slower than a default group by.
            Settings this to `True` blocks the possibility
            to run on the streaming engine.

            .. note::
                Within each group, the order of rows is always preserved, regardless
                of this argument.

        Returns
        -------
        GroupBy
            Object which can be used to perform aggregations.

        """
        return self.group_by(by, *more_by, maintain_order=maintain_order)
