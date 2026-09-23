    def __init__(self, obj, n, keep, columns):
        super().__init__(obj, n, keep)
        if not is_list_like(columns) or isinstance(columns, tuple):
            columns = [columns]
        columns = list(columns)
        self.columns = columns
