    def __init__(self, obj, n, keep, columns):
        super(SelectNFrame, self).__init__(obj, n, keep)
        if not is_list_like(columns):
            columns = [columns]
        columns = list(columns)
        self.columns = columns
