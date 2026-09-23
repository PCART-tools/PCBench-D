    def __init__(self, num_steps, column_names=None):
        super().__init__(num_steps)
        self.inner_table = None if column_names is None else [column_names]
        self.child_bar = None
