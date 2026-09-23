    @cbook.deprecated("2.1", alternative="canvas.draw_idle")
    def dynamic_update(self):
        self.canvas.draw_idle()
