    def _onmove(self, event):
        """Cursor move event handler."""
        # Move the active vertex (ToolHandle).
        if self._active_handle_idx >= 0:
            idx = self._active_handle_idx
            self._xs[idx], self._ys[idx] = event.xdata, event.ydata
            # Also update the end of the polygon line if the first vertex is
            # the active handle and the polygon is completed.
            if idx == 0 and self._selection_completed:
                self._xs[-1], self._ys[-1] = event.xdata, event.ydata

        # Move all vertices.
        elif 'move_all' in self._state and self._eventpress:
            dx = event.xdata - self._eventpress.xdata
            dy = event.ydata - self._eventpress.ydata
            for k in range(len(self._xs)):
                self._xs[k] = self._xs_at_press[k] + dx
                self._ys[k] = self._ys_at_press[k] + dy

        # Do nothing if completed or waiting for a move.
        elif (self._selection_completed
              or 'move_vertex' in self._state or 'move_all' in self._state):
            return

        # Position pending vertex.
        else:
            # Calculate distance to the start vertex.
            x0, y0 = self._selection_artist.get_transform().transform(
                    (self._xs[0], self._ys[0])
                )
            v0_dist = np.hypot(x0 - event.x, y0 - event.y)
            # Lock on to the start vertex if near it and ready to complete.
            if len(self._xs) > 3 and v0_dist < self.grab_range:
                self._xs[-1], self._ys[-1] = self._xs[0], self._ys[0]
            else:
                self._xs[-1], self._ys[-1] = event.xdata, event.ydata

        self._draw_polygon()
