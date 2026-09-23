    def __init__(
        self,
        data: Series,
        memory_usage: bool | str | None = None,
    ) -> None:
        self.data: Series = data
        self.memory_usage = _initialize_memory_usage(memory_usage)
