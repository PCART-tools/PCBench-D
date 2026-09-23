    def __setstate__(self, state: list[Any]) -> None:
        self.layers, self.layer = state[6:]
        super().__setstate__(state)
