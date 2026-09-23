    def _set_cursor(self, enabled):
        """Update the canvas cursor based on direction of the selector."""
        if enabled:
            cursor = (backend_tools.Cursors.RESIZE_HORIZONTAL
                      if self.direction == 'horizontal' else
                      backend_tools.Cursors.RESIZE_VERTICAL)
        else:
            cursor = backend_tools.Cursors.POINTER

        self.ax.get_figure(root=True).canvas.set_cursor(cursor)
