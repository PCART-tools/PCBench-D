    def __init__(self, obj, n: int, keep: str, columns):
        super().__init__(obj, n, keep)
        if not is_list_like(columns) or isinstance(columns, tuple):
            columns = [columns]
        columns = list(columns)
        self.columns = columns
