    def pop_click(self, event, index=-1):
        """Remove a click (by default, the last) from the list of clicks."""
        self.clicks.pop(index)
        if self.show_clicks:
            self.marks.pop(index).remove()
            self.fig.canvas.draw()
