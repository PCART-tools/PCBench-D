    def get_bbox(self, renderer):
        """Return the bbox of the offsetbox, ignoring parent offsets."""
        bbox, offsets = self._get_bbox_and_child_offsets(renderer)
        return bbox
