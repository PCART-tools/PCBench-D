    @deprecate_function(
        "Use `unpivot` instead, with `index` instead of `id_vars` and `on` instead of `value_vars`",
        version="1.0.0",
    )
    def melt(
        self,
        id_vars: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        value_vars: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        variable_name: str | None = None,
        value_name: str | None = None,
        *,
        streamable: bool = True,
    ) -> LazyFrame:
        """
        Unpivot a DataFrame from wide to long format.

        Optionally leaves identifiers set.

        This function is useful to massage a DataFrame into a format where one or more
        columns are identifier variables (id_vars) while all other columns, considered
        measured variables (value_vars), are "unpivoted" to the row axis leaving just
        two non-identifier columns, 'variable' and 'value'.

        .. deprecated 1.0.0
            Please use :meth:`.unpivot` instead.

        Parameters
        ----------
        id_vars
            Column(s) or selector(s) to use as identifier variables.
        value_vars
            Column(s) or selector(s) to use as values variables; if `value_vars`
            is empty all columns that are not in `id_vars` will be used.
        variable_name
            Name to give to the `variable` column. Defaults to "variable"
        value_name
            Name to give to the `value` column. Defaults to "value"
        streamable
            Allow this node to run in the streaming engine.
            If this runs in streaming, the output of the unpivot operation
            will not have a stable ordering.
        """
        return self.unpivot(
            index=id_vars,
            on=value_vars,
            variable_name=variable_name,
            value_name=value_name,
            streamable=streamable,
        )
