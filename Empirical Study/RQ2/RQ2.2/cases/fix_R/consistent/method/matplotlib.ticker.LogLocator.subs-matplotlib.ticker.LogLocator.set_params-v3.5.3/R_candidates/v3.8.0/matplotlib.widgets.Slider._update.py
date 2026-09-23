    def _update(self, event):
        """Update the slider position."""
        if self.ignore(event) or event.button != 1:
            return

        if event.name == 'button_press_event' and self.ax.contains(event)[0]:
            self.drag_active = True
            event.canvas.grab_mouse(self.ax)

        if not self.drag_active:
            return

        if (event.name == 'button_release_event'
              or event.name == 'button_press_event' and not self.ax.contains(event)[0]):
            self.drag_active = False
            event.canvas.release_mouse(self.ax)
            return

        xdata, ydata = self._get_data_coords(event)
        val = self._value_in_bounds(
            xdata if self.orientation == 'horizontal' else ydata)
        if val not in [None, self.val]:
            self.set_val(val)
