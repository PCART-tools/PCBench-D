    def press_zoom(self, event):
        """Callback for mouse button press in zoom to rect mode."""
        if (event.button not in [MouseButton.LEFT, MouseButton.RIGHT]
                or event.x is None or event.y is None):
            return

        axes = self._start_event_axes_interaction(event, method="zoom")
        if not axes:
            return

        id_zoom = self.canvas.mpl_connect(
            "motion_notify_event", self.drag_zoom)

        # A colorbar is one-dimensional, so we extend the zoom rectangle out
        # to the edge of the Axes bbox in the other dimension. To do that we
        # store the orientation of the colorbar for later.
        parent_ax = axes[0]
        if hasattr(parent_ax, "_colorbar"):
            cbar = parent_ax._colorbar.orientation
        else:
            cbar = None

        self._zoom_info = self._ZoomInfo(
            direction="in" if event.button == 1 else "out",
            start_xy=(event.x, event.y), axes=axes, cid=id_zoom, cbar=cbar)
