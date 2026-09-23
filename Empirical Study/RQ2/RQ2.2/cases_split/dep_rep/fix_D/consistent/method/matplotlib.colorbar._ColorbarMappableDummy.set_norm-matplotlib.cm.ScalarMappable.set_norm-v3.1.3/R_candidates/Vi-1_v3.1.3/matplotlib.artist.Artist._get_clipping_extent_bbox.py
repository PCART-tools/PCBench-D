    def _get_clipping_extent_bbox(self):
        """
        Return a bbox with the extents of the intersection of the clip_path
        and clip_box for this artist, or None if both of these are
        None, or ``get_clip_on`` is False.
        """
        bbox = None
        if self.get_clip_on():
            clip_box = self.get_clip_box()
            if clip_box is not None:
                bbox = clip_box
            clip_path = self.get_clip_path()
            if clip_path is not None and bbox is not None:
                clip_path = clip_path.get_fully_transformed_path()
                bbox = Bbox.intersection(bbox, clip_path.get_extents())
        return bbox
