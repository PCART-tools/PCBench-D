    @_api.deprecated("3.3", alternative="toolbar.canvas.draw_idle()")
    def draw(self):
        """Redraw the canvases, update the locators."""
        self._draw()
