    def get_window_extent(self, renderer=None):
        # docstring inherited
        # This block is the same as in Text.get_window_extent, but we need to
        # set the renderer before calling update_positions().
        if not self.get_visible() or not self._check_xy(renderer):
            return Bbox.unit()
        if renderer is not None:
            self._renderer = renderer
        if self._renderer is None:
            self._renderer = self.figure._get_renderer()
        if self._renderer is None:
            raise RuntimeError('Cannot get window extent w/o renderer')

        self.update_positions(self._renderer)

        text_bbox = Text.get_window_extent(self)
        bboxes = [text_bbox]

        if self.arrow_patch is not None:
            bboxes.append(self.arrow_patch.get_window_extent())

        return Bbox.union(bboxes)
