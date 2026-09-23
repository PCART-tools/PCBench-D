    def _get_bbox_and_child_offsets(self, renderer):
        # docstring inherited
        dpicor = renderer.points_to_pixels(1.)
        pad = self.pad * dpicor
        sep = self.sep * dpicor

        bboxes = [c.get_bbox(renderer) for c in self.get_visible_children()]
        if not bboxes:
            return Bbox.from_bounds(0, 0, 0, 0).padded(pad), []

        (y0, y1), yoffsets = _get_aligned_offsets(
            [bbox.intervaly for bbox in bboxes], self.height, self.align)
        width, xoffsets = _get_packed_offsets(
            [bbox.width for bbox in bboxes], self.width, sep, self.mode)

        x0 = bboxes[0].x0
        xoffsets -= ([bbox.x0 for bbox in bboxes] - x0)

        return (Bbox.from_bounds(x0, y0, width, y1 - y0).padded(pad),
                [*zip(xoffsets, yoffsets)])
