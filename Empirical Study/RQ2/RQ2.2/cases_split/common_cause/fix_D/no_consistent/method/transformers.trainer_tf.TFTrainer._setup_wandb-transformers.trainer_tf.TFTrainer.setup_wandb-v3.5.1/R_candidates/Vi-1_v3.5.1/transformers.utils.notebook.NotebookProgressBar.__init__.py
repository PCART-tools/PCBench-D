    def __init__(
        self,
        total: int,
        prefix: Optional[str] = None,
        leave: bool = True,
        parent: Optional["NotebookTrainingTracker"] = None,
        width: int = 300,
    ):
        self.total = total
        self.prefix = "" if prefix is None else prefix
        self.leave = leave
        self.parent = parent
        self.width = width
        self.last_value = None
        self.comment = None
        self.output = None
