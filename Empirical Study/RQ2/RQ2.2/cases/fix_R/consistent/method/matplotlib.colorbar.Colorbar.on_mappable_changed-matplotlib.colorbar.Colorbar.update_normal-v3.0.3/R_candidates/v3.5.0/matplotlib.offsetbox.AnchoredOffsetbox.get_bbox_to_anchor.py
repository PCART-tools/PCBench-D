    def get_bbox_to_anchor(self):
        """Return the bbox that the box is anchored to."""
        if self._bbox_to_anchor is None:
            return self.axes.bbox
        else:
            transform = self._bbox_to_anchor_transform
            if transform is None:
                return self._bbox_to_anchor
            else:
                return TransformedBbox(self._bbox_to_anchor,
                                       transform)
