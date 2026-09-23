    def _release(self, event):
        """Button release event handler."""
        # Release active tool handle.
        if self._active_handle_idx >= 0:
            if event.button == 3:
                self._remove_vertex(self._active_handle_idx)
                self._draw_polygon()
            self._active_handle_idx = -1

        # Complete the polygon.
        elif (len(self._xs) > 3
              and self._xs[-1] == self._xs[0]
              and self._ys[-1] == self._ys[0]):
            self._selection_completed = True

        # Place new vertex.
        elif (not self._selection_completed
              and 'move_all' not in self._state
              and 'move_vertex' not in self._state):
            self._xs.insert(-1, event.xdata)
            self._ys.insert(-1, event.ydata)

        if self._selection_completed:
            self.onselect(self.verts)
