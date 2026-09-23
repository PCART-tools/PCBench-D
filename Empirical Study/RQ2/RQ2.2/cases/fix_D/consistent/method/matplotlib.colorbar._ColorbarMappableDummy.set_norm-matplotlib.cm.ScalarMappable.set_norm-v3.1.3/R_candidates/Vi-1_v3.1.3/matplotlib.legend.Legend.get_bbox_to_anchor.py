    def get_bbox_to_anchor(self):
        """Return the bbox that the legend will be anchored to."""
        if self._bbox_to_anchor is None:
            return self.parent.bbox
        else:
            return self._bbox_to_anchor
