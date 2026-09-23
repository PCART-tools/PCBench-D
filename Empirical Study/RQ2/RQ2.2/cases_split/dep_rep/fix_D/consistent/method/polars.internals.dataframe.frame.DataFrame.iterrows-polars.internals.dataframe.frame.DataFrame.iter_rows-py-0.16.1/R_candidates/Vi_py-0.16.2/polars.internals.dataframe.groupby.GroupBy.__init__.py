    def __init__(
        self,
        df: PyDataFrame,
        by: str | pli.Expr | Sequence[str | pli.Expr],
        dataframe_class: type[DF],
        maintain_order: bool,
    ):
        """
        Construct class representing a group by operation over the given dataframe.

        Parameters
        ----------
        df
            PyDataFrame to perform operation over.
        by
            Column(s) to group by.
        dataframe_class
            The class used to wrap around the given dataframe. Used to construct new
            dataframes returned from the group by operation.
        maintain_order
            Make sure that the order of the groups remain consistent. This is more
            expensive than a default groupby. Note that this only works in expression
            aggregations.

        """
        self._df = df
        self._dataframe_class = dataframe_class
        self.by = by
        self.maintain_order = maintain_order
