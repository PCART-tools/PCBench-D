    def _mouse_event_coords(self, event):
        """
        Calculate mouse coordinates in physical pixels.

        GTK use logical pixels, but the figure is scaled to physical pixels for
        rendering.  Transform to physical pixels so that all of the down-stream
        transforms work as expected.

        Also, the origin is different and needs to be corrected.
        """
        x = event.x * self.device_pixel_ratio
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y * self.device_pixel_ratio
        return x, y
