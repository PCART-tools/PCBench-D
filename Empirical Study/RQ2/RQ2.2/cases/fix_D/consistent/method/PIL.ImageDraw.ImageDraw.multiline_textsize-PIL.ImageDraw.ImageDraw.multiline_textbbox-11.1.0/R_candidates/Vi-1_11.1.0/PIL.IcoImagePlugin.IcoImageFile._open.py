    def _open(self) -> None:
        self.ico = IcoFile(self.fp)
        self.info["sizes"] = self.ico.sizes()
        self.size = self.ico.entry[0].dim
        self.load()
