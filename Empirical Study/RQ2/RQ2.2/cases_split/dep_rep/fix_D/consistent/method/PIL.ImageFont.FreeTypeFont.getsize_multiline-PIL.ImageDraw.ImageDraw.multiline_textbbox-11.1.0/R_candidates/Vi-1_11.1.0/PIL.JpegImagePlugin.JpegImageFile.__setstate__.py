    def __setstate__(self, state: list[Any]) -> None:
        super().__setstate__(state)
        self.layers, self.layer = state[5:]
