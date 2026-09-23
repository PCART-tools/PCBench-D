    def blit(self, bbox=None):
        tkagg.blit(self._tkphoto, self.renderer._renderer, bbox=bbox, colormode=2)
        self._master.update_idletasks()
