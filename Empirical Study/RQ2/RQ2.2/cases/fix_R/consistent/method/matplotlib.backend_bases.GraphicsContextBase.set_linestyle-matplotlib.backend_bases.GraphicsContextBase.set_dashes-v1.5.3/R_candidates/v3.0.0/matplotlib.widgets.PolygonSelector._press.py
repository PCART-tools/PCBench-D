    def _press(self, event):
        """Button press event handler"""
        # Check for selection of a tool handle.
        if ((self._polygon_completed or 'move_vertex' in self.state)
                and len(self._xs) > 0):
            h_idx, h_dist = self._polygon_handles.closest(event.x, event.y)
            if h_dist < self.vertex_select_radius:
                self._active_handle_idx = h_idx
        # Save the vertex positions at the time of the press event (needed to
        # support the 'move_all' state modifier).
        self._xs_at_press, self._ys_at_press = self._xs[:], self._ys[:]
