    @staticmethod
    def from_bounds(x0, y0, width, height):
        """
        Create a new `Bbox` from *x0*, *y0*, *width* and *height*.

        *width* and *height* may be negative.
        """
        return Bbox.from_extents(x0, y0, x0 + width, y0 + height)
