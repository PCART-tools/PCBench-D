    def mouseEventCoords(self, pos):
        """
        Calculate mouse coordinates in physical pixels.

        Qt uses logical pixels, but the figure is scaled to physical
        pixels for rendering.  Transform to physical pixels so that
        all of the down-stream transforms work as expected.

        Also, the origin is different and needs to be corrected.
        """
        x = pos.x()
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height / self.device_pixel_ratio - pos.y()
        return x * self.device_pixel_ratio, y * self.device_pixel_ratio
