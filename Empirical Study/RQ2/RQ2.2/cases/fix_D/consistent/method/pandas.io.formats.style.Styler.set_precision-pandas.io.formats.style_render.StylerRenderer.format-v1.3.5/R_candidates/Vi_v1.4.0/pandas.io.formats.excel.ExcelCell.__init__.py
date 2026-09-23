    def __init__(
        self,
        row: int,
        col: int,
        val,
        style=None,
        mergestart: int | None = None,
        mergeend: int | None = None,
    ):
        self.row = row
        self.col = col
        self.val = val
        self.style = style
        self.mergestart = mergestart
        self.mergeend = mergeend
