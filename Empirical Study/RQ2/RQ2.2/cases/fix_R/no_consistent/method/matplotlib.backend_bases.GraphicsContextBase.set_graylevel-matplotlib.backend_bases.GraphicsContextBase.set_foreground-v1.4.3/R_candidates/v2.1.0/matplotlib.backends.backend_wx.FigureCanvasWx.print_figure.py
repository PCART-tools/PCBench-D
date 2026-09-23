    def print_figure(self, filename, *args, **kwargs):
        # Use pure Agg renderer to draw
        FigureCanvasBase.print_figure(self, filename, *args, **kwargs)
        # Restore the current view; this is needed because the
        # artist contains methods rely on particular attributes
        # of the rendered figure for determining things like
        # bounding boxes.
        if self._isDrawn:
            self.draw()
