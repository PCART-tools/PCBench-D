    def _update(self, event):
        """Update the slider position."""
        if self.ignore(event) or event.button != 1:
            return

        if event.name == "button_press_event" and self.ax.contains(event)[0]:
            self.drag_active = True
            event.canvas.grab_mouse(self.ax)

        if not self.drag_active:
            return

        if (event.name == "button_release_event"
              or event.name == "button_press_event" and not self.ax.contains(event)[0]):
            self.drag_active = False
            event.canvas.release_mouse(self.ax)
            self._active_handle = None
            return

        # determine which handle was grabbed
        xdata, ydata = self._get_data_coords(event)
        handle_index = np.argmin(np.abs(
            [h.get_xdata()[0] - xdata for h in self._handles]
            if self.orientation == "horizontal" else
            [h.get_ydata()[0] - ydata for h in self._handles]))
        handle = self._handles[handle_index]

        # these checks ensure smooth behavior if the handles swap which one
        # has a higher value. i.e. if one is dragged over and past the other.
        if handle is not self._active_handle:
            self._active_handle = handle

        self._update_val_from_pos(xdata if self.orientation == "horizontal" else ydata)
