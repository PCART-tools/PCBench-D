    def _repr_html_(self, **kwargs: Any) -> str:
        """
        Format output data in HTML for display in Jupyter Notebooks.

        Output rows and columns can be modified by setting the following ENVIRONMENT
        variables:

        * POLARS_FMT_MAX_COLS: set the number of columns
        * POLARS_FMT_MAX_ROWS: set the number of rows

        """
        max_cols = int(os.environ.get("POLARS_FMT_MAX_COLS", default=75))
        if max_cols < 0:
            max_cols = self.shape[1]
        max_rows = int(os.environ.get("POLARS_FMT_MAX_ROWS", default=25))
        if max_rows < 0:
            max_rows = self.shape[0]

        from_series = kwargs.get("from_series", False)
        return "\n".join(
            NotebookFormatter(
                self,
                max_cols=max_cols,
                max_rows=max_rows,
                from_series=from_series,
            ).render()
        )
