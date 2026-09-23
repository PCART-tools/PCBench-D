    def set_bbox_to_anchor(self, bbox, transform=None):
        """
        Set the bbox that the legend will be anchored to.

        *bbox* can be

        - A `.BboxBase` instance
        - A tuple of ``(left, bottom, width, height)`` in the given transform
          (normalized axes coordinate if None)
        - A tuple of ``(left, bottom)`` where the width and height will be
          assumed to be zero.
        """
        if bbox is None:
            self._bbox_to_anchor = None
            return
        elif isinstance(bbox, BboxBase):
            self._bbox_to_anchor = bbox
        else:
            try:
                l = len(bbox)
            except TypeError:
                raise ValueError("Invalid argument for bbox : %s" % str(bbox))

            if l == 2:
                bbox = [bbox[0], bbox[1], 0, 0]

            self._bbox_to_anchor = Bbox.from_bounds(*bbox)

        if transform is None:
            transform = BboxTransformTo(self.parent.bbox)

        self._bbox_to_anchor = TransformedBbox(self._bbox_to_anchor,
                                               transform)
        self.stale = True
