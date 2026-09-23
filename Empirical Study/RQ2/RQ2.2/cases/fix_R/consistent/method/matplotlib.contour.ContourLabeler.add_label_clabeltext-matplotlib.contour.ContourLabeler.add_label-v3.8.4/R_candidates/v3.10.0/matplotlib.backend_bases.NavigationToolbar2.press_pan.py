    def press_pan(self, event):
        """Callback for mouse button press in pan/zoom mode."""
        if (event.button not in [MouseButton.LEFT, MouseButton.RIGHT]
                or event.x is None or event.y is None):
            return

        axes = self._start_event_axes_interaction(event, method="pan")
        if not axes:
            return

        # call "ax.start_pan(..)" on all relevant axes of an event
        for ax in axes:
            ax.start_pan(event.x, event.y, event.button)

        self.canvas.mpl_disconnect(self._id_drag)
        id_drag = self.canvas.mpl_connect("motion_notify_event", self.drag_pan)

        self._pan_info = self._PanInfo(
            button=event.button, axes=axes, cid=id_drag)
