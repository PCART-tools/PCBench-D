    def _hover(self, event):
        """Update the canvas cursor if it's over a handle."""
        if self.ignore(event):
            return

        if self._active_handle is not None or not self._selection_completed:
            # Do nothing if button is pressed and a handle is active, which may
            # occur with drag_from_anywhere=True.
            # Do nothing if selection is not completed, which occurs when
            # a selector has been cleared
            return

        _, e_dist = self._edge_handles.closest(event.x, event.y)
        self._set_cursor(e_dist <= self.grab_range)
