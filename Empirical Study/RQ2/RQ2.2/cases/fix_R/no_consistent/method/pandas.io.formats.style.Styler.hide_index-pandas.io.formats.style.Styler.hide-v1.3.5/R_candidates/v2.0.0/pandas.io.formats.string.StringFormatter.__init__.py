    def __init__(self, fmt: DataFrameFormatter, line_width: int | None = None) -> None:
        self.fmt = fmt
        self.adj = fmt.adj
        self.frame = fmt.frame
        self.line_width = line_width
