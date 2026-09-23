    def __init__(
        self,
        formatter: DataFrameFormatter,
        longtable: bool = False,
        column_format: str | None = None,
        multicolumn: bool = False,
        multicolumn_format: str | None = None,
        multirow: bool = False,
        caption: str | tuple[str, str] | None = None,
        label: str | None = None,
        position: str | None = None,
    ):
        self.fmt = formatter
        self.frame = self.fmt.frame
        self.longtable = longtable
        self.column_format = column_format
        self.multicolumn = multicolumn
        self.multicolumn_format = multicolumn_format
        self.multirow = multirow
        self.caption, self.short_caption = _split_into_full_short_caption(caption)
        self.label = label
        self.position = position
