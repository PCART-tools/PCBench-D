    def _update_offset_func(self, renderer, fontsize=None):
        """
        Update the offset func which depends on the dpi of the
        renderer (because of the padding).
        """
        if fontsize is None:
            fontsize = renderer.points_to_pixels(
                self.prop.get_size_in_points())

        def _offset(w, h, xd, yd, renderer):
            bbox = Bbox.from_bounds(0, 0, w, h)
            borderpad = self.borderpad * fontsize
            bbox_to_anchor = self.get_bbox_to_anchor()
            x0, y0 = _get_anchored_bbox(
                self.loc, bbox, bbox_to_anchor, borderpad)
            return x0 + xd, y0 + yd

        self.set_offset(_offset)
