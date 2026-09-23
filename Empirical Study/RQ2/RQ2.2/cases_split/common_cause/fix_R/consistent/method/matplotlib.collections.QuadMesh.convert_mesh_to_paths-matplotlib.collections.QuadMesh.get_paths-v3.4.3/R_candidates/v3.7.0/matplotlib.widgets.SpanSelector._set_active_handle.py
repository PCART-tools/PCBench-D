    def _set_active_handle(self, event):
        """Set active handle based on the location of the mouse event."""
        # Note: event.xdata/ydata in data coordinates, event.x/y in pixels
        e_idx, e_dist = self._edge_handles.closest(event.x, event.y)

        # Prioritise center handle over other handles
        # Use 'C' to match the notation used in the RectangleSelector
        if 'move' in self._state:
            self._active_handle = 'C'
        elif e_dist > self.grab_range:
            # Not close to any handles
            self._active_handle = None
            if self.drag_from_anywhere and self._contains(event):
                # Check if we've clicked inside the region
                self._active_handle = 'C'
                self._extents_on_press = self.extents
            else:
                self._active_handle = None
                return
        else:
            # Closest to an edge handle
            self._active_handle = self._edge_order[e_idx]

        # Save coordinates of rectangle at the start of handle movement.
        self._extents_on_press = self.extents
