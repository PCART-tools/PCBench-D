    @cbook.deprecated("3.3", alternative="self.figure.canvas.draw_idle()")
    def refresh_locators(self):
        """Redraw the canvases, update the locators."""
        self._refresh_locators()
