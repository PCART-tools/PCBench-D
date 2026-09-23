    def __setstate__(self, state: list[Any]) -> None:
        self.tile = []
        super().__setstate__(state)
