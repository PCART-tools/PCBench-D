    def _copy(self) -> None:
        self.load()
        self.im = self.im.copy()
        self.pyaccess = None
        self.readonly = 0
