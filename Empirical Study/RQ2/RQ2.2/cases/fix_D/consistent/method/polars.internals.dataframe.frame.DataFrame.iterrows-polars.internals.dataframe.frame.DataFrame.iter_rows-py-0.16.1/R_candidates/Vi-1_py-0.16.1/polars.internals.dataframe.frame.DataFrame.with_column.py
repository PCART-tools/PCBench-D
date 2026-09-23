    def with_column(self, column: pli.Series | pli.Expr) -> DataFrame:
        """
        Return a new DataFrame with the column added, if new, or replaced.

        Notes
        -----
        Creating a new DataFrame using this method does not create a new copy of
        existing data.

        .. deprecated:: 0.15.14
            `with_column` will be removed in favor of the more generic `with_columns`
            in version 0.17.0.

        Parameters
        ----------
        column
            Series, where the name of the Series refers to the column in the DataFrame.

        """
        warnings.warn(
            "`with_column` has been deprecated in favor of `with_columns`."
            " This method will be removed in version 0.17.0",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.lazy().with_columns(column).collect(no_optimization=True)
