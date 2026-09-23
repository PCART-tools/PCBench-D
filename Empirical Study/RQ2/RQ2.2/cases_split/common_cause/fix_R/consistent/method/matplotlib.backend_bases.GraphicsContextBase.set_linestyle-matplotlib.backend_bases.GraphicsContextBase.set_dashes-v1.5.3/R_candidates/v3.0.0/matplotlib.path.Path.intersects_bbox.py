    def intersects_bbox(self, bbox, filled=True):
        """
        Returns *True* if this path intersects a given
        :class:`~matplotlib.transforms.Bbox`.

        *filled*, when True, treats the path as if it was filled.
        That is, if the path completely encloses the bounding box,
        :meth:`intersects_bbox` will return True.

        The bounding box is always considered filled.
        """
        return _path.path_intersects_rectangle(self,
            bbox.x0, bbox.y0, bbox.x1, bbox.y1, filled)
