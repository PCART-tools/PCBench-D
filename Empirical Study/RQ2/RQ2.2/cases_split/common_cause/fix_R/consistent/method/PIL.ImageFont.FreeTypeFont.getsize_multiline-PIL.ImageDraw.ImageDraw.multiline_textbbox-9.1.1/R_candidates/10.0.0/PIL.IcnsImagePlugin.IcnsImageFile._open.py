    def _open(self):
        self.icns = IcnsFile(self.fp)
        self.mode = "RGBA"
        self.info["sizes"] = self.icns.itersizes()
        self.best_size = self.icns.bestsize()
        self.size = (
            self.best_size[0] * self.best_size[2],
            self.best_size[1] * self.best_size[2],
        )
