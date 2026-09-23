    @_compat_get_offset
    def get_offset(self, bbox, renderer):
        # docstring inherited
        pad = (self.borderpad
               * renderer.points_to_pixels(self.prop.get_size_in_points()))
        bbox_to_anchor = self.get_bbox_to_anchor()
        x0, y0 = _get_anchored_bbox(
            self.loc, Bbox.from_bounds(0, 0, bbox.width, bbox.height),
            bbox_to_anchor, pad)
        return x0 - bbox.x0, y0 - bbox.y0
