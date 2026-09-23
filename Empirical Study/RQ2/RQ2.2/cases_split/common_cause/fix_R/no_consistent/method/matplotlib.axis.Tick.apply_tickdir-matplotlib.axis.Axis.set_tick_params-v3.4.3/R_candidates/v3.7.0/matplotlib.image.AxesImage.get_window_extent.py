    def get_window_extent(self, renderer=None):
        x0, x1, y0, y1 = self._extent
        bbox = Bbox.from_extents([x0, y0, x1, y1])
        return bbox.transformed(self.get_transform())
