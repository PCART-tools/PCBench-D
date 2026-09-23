    def get_bbox(self):
        return transforms.Bbox.from_bounds(self._x, self._y,
                                           self._width, self._height)
