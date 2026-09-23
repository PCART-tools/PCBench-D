    def __setstate__(self, state: list[Any]) -> None:
        self.tile = []
        self.filename = state[5]
        super().__setstate__(state)
