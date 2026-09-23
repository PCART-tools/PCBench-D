    def get_bbox(self):
        """Return the `.Bbox`."""
        x0, y0, x1, y1 = self._convert_units()
        return transforms.Bbox.from_extents(x0, y0, x1, y1)
