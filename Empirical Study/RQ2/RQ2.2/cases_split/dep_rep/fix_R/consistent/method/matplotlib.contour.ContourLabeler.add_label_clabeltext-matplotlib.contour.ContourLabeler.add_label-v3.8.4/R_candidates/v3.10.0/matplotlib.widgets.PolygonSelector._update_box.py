    def _update_box(self):
        # Update selection box extents to the extents of the polygon
        if self._box is not None:
            bbox = self._get_bbox()
            self._box.extents = [bbox.x0, bbox.x1, bbox.y0, bbox.y1]
            # Save a copy
            self._old_box_extents = self._box.extents
