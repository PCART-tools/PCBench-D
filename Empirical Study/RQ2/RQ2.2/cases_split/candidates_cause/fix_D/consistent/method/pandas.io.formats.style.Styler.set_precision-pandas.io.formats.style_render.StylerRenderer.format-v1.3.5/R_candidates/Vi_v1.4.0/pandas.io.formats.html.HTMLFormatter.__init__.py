    def __init__(
        self,
        formatter: DataFrameFormatter,
        classes: str | list[str] | tuple[str, ...] | None = None,
        border: int | None = None,
        table_id: str | None = None,
        render_links: bool = False,
    ) -> None:
        self.fmt = formatter
        self.classes = classes

        self.frame = self.fmt.frame
        self.columns = self.fmt.tr_frame.columns
        self.elements: list[str] = []
        self.bold_rows = self.fmt.bold_rows
        self.escape = self.fmt.escape
        self.show_dimensions = self.fmt.show_dimensions
        if border is None:
            border = cast(int, get_option("display.html.border"))
        self.border = border
        self.table_id = table_id
        self.render_links = render_links

        self.col_space = {
            column: f"{value}px" if isinstance(value, int) else value
            for column, value in self.fmt.col_space.items()
        }
