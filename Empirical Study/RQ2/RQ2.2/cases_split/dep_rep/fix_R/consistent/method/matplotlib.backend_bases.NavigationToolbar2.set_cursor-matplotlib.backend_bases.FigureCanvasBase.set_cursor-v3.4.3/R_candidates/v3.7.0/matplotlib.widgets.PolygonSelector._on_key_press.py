    def _on_key_press(self, event):
        """Key press event handler."""
        # Remove the pending vertex if entering the 'move_vertex' or
        # 'move_all' mode
        if (not self._selection_completed
                and ('move_vertex' in self._state or
                     'move_all' in self._state)):
            self._xys.pop()
            self._draw_polygon()
