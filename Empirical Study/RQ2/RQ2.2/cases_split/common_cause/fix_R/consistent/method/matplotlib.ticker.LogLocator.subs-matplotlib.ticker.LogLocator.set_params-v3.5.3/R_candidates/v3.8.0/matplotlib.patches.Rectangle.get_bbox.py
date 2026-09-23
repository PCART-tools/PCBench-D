    def get_bbox(self):
        """Return the `.Bbox`."""
        return transforms.Bbox.from_extents(*self._convert_units())
