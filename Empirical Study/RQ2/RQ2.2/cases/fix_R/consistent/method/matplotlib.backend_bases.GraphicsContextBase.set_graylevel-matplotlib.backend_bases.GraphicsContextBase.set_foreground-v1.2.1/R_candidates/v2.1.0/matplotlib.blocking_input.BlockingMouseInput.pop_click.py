    def pop_click(self, event, index=-1):
        """
        This removes a click from the list of clicks.  Defaults to
        removing the last click.
        """
        self.clicks.pop(index)

        if self.show_clicks:

            mark = self.marks.pop(index)
            mark.remove()

            self.fig.canvas.draw()
