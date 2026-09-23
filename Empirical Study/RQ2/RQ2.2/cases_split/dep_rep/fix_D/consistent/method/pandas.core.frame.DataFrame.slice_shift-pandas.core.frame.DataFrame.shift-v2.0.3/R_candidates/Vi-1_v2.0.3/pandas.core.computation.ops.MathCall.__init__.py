    def __init__(self, func, args) -> None:
        super().__init__(func.name, args)
        self.func = func
