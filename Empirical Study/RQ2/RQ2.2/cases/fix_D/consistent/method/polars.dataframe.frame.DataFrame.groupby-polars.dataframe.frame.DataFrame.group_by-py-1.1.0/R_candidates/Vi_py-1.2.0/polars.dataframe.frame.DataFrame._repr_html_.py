    def _repr_html_(self, *, _from_series: bool = False) -> str:
        """
        Format output data in HTML for display in Jupyter Notebooks.

        Output rows and columns can be modified by setting the following ENVIRONMENT
        variables:

        * POLARS_FMT_MAX_COLS: set the number of columns
        * POLARS_FMT_MAX_ROWS: set the number of rows
        """
        max_cols = int(os.environ.get("POLARS_FMT_MAX_COLS", default=75))
        if max_cols < 0:
            max_cols = self.width

        max_rows = int(os.environ.get("POLARS_FMT_MAX_ROWS", default=10))
        if max_rows < 0:
            max_rows = self.height

        return "".join(
            NotebookFormatter(
                self,
                max_cols=max_cols,
                max_rows=max_rows,
                from_series=_from_series,
            ).render()
        )
