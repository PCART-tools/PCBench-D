    def __init__(
        self,
        data: DataFrame,
        memory_usage: bool | str | None = None,
    ) -> None:
        self.data: DataFrame = data
        self.memory_usage = _initialize_memory_usage(memory_usage)
