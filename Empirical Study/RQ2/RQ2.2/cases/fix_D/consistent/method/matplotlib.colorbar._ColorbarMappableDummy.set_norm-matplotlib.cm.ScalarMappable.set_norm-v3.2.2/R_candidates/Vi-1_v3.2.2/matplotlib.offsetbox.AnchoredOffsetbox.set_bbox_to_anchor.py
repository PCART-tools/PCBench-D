    def set_bbox_to_anchor(self, bbox, transform=None):
        """
        set the bbox that the child will be anchored.

        *bbox* can be a Bbox instance, a list of [left, bottom, width,
        height], or a list of [left, bottom] where the width and
        height will be assumed to be zero. The bbox will be
        transformed to display coordinate by the given transform.
        """
        if bbox is None or isinstance(bbox, BboxBase):
            self._bbox_to_anchor = bbox
        else:
            try:
                l = len(bbox)
            except TypeError:
                raise ValueError("Invalid argument for bbox : %s" % str(bbox))

            if l == 2:
                bbox = [bbox[0], bbox[1], 0, 0]

            self._bbox_to_anchor = Bbox.from_bounds(*bbox)

        self._bbox_to_anchor_transform = transform
        self.stale = True
