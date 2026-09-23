    def draw(self):
        FigureCanvasAgg.draw(self)
        tkagg.blit(self._tkphoto, self.renderer._renderer, colormode=2)
        self._master.update_idletasks()
