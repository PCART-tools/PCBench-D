    def _update(self, event):
        """Update the slider position."""
        if self.ignore(event) or event.button != 1:
            return

        if event.name == "button_press_event" and event.inaxes == self.ax:
            self.drag_active = True
            event.canvas.grab_mouse(self.ax)

        if not self.drag_active:
            return

        elif (event.name == "button_release_event") or (
            event.name == "button_press_event" and event.inaxes != self.ax
        ):
            self.drag_active = False
            event.canvas.release_mouse(self.ax)
            return
        if self.orientation == "vertical":
            self._update_val_from_pos(event.ydata)
        else:
            self._update_val_from_pos(event.xdata)
