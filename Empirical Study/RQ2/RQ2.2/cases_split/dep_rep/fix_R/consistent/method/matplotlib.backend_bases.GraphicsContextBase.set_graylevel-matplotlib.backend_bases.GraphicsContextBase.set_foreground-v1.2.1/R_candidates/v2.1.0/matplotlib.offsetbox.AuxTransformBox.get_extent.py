    def get_extent(self, renderer):

        # clear the offset transforms
        _off = self.offset_transform.to_values()  # to be restored later
        self.ref_offset_transform.clear()
        self.offset_transform.clear()

        # calculate the extent
        bboxes = [c.get_window_extent(renderer) for c in self._children]
        ub = mtransforms.Bbox.union(bboxes)

        # adjust ref_offset_tansform
        self.ref_offset_transform.translate(-ub.x0, -ub.y0)

        # restor offset transform
        mtx = self.offset_transform.matrix_from_values(*_off)
        self.offset_transform.set_matrix(mtx)

        return ub.width, ub.height, 0., 0.
