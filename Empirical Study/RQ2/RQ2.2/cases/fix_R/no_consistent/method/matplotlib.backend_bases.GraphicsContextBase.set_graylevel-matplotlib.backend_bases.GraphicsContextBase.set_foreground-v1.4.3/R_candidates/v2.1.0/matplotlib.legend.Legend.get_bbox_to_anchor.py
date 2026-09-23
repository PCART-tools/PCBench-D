    def get_bbox_to_anchor(self):
        """
        return the bbox that the legend will be anchored
        """
        if self._bbox_to_anchor is None:
            return self.parent.bbox
        else:
            return self._bbox_to_anchor
