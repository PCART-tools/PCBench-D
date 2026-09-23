    def drag_zoom(self, event):
        """Callback for dragging in zoom mode."""
        start_xy = self._zoom_info.start_xy
        ax = self._zoom_info.axes[0]
        (x1, y1), (x2, y2) = np.clip(
            [start_xy, [event.x, event.y]], ax.bbox.min, ax.bbox.max)
        if event.key == "x":
            y1, y2 = ax.bbox.intervaly
        elif event.key == "y":
            x1, x2 = ax.bbox.intervalx
        self.draw_rubberband(event, x1, y1, x2, y2)
