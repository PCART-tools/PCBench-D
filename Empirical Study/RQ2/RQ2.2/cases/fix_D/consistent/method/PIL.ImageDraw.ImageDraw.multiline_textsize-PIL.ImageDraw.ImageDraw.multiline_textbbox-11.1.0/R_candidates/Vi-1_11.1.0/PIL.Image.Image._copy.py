    def _copy(self) -> None:
        self.load()
        self.im = self.im.copy()
        self.readonly = 0
