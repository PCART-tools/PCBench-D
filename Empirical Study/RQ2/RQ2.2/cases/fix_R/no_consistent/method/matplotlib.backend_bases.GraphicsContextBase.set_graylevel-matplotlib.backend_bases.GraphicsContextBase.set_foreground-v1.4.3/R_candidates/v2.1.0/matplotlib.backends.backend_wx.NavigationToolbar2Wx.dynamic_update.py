    @cbook.deprecated("2.1", alternative="canvas.draw_idle")
    def dynamic_update(self):
        d = self._idle
        self._idle = False
        if d:
            self.canvas.draw()
            self._idle = True
