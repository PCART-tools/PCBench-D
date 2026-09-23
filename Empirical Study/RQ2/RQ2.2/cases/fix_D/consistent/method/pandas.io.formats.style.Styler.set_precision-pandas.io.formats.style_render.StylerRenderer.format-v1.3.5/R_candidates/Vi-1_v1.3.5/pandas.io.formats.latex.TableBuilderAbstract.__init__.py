    def __init__(
        self,
        formatter: DataFrameFormatter,
        column_format: str | None = None,
        multicolumn: bool = False,
        multicolumn_format: str | None = None,
        multirow: bool = False,
        caption: str | None = None,
        short_caption: str | None = None,
        label: str | None = None,
        position: str | None = None,
    ):
        self.fmt = formatter
        self.column_format = column_format
        self.multicolumn = multicolumn
        self.multicolumn_format = multicolumn_format
        self.multirow = multirow
        self.caption = caption
        self.short_caption = short_caption
        self.label = label
        self.position = position
