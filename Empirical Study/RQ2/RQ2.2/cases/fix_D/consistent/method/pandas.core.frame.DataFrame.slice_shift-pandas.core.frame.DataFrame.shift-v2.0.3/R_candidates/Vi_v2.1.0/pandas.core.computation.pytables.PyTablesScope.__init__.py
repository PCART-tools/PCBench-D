    def __init__(
        self,
        level: int,
        global_dict=None,
        local_dict=None,
        queryables: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(level + 1, global_dict=global_dict, local_dict=local_dict)
        self.queryables = queryables or {}
