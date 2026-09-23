    def __init__(
        self,
        df,
        na_rep: str = "",
        float_format: str | None = None,
        cols: Sequence[Hashable] | None = None,
        header: Sequence[Hashable] | bool = True,
        index: bool = True,
        index_label: IndexLabel | None = None,
        merge_cells: bool = False,
        inf_rep: str = "inf",
        style_converter: Callable | None = None,
    ) -> None:
        self.rowcounter = 0
        self.na_rep = na_rep
        if not isinstance(df, DataFrame):
            self.styler = df
            self.styler._compute()  # calculate applied styles
            df = df.data
            if style_converter is None:
                style_converter = CSSToExcelConverter()
            self.style_converter: Callable | None = style_converter
        else:
            self.styler = None
            self.style_converter = None
        self.df = df
        if cols is not None:
            # all missing, raise
            if not len(Index(cols).intersection(df.columns)):
                raise KeyError("passes columns are not ALL present dataframe")

            if len(Index(cols).intersection(df.columns)) != len(set(cols)):
                # Deprecated in GH#17295, enforced in 1.0.0
                raise KeyError("Not all names specified in 'columns' are found")

            self.df = df.reindex(columns=cols)

        self.columns = self.df.columns
        self.float_format = float_format
        self.index = index
        self.index_label = index_label
        self.header = header
        self.merge_cells = merge_cells
        self.inf_rep = inf_rep
