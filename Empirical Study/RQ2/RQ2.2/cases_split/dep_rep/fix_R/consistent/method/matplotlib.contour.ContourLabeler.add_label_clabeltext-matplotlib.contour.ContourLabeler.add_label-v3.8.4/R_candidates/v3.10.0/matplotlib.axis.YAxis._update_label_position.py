    def _update_label_position(self, renderer):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        if not self._autolabelpos:
            return

        # get bounding boxes for this axis and any siblings
        # that have been set by `fig.align_ylabels()`
        bboxes, bboxes2 = self._get_tick_boxes_siblings(renderer=renderer)
        x, y = self.label.get_position()

        if self.label_position == 'left':
            # Union with extents of the left spine if present, of the axes otherwise.
            bbox = mtransforms.Bbox.union([
                *bboxes, self.axes.spines.get("left", self.axes).get_window_extent()])
            self.label.set_position(
                (bbox.x0 - self.labelpad * self.get_figure(root=True).dpi / 72, y))
        else:
            # Union with extents of the right spine if present, of the axes otherwise.
            bbox = mtransforms.Bbox.union([
                *bboxes2, self.axes.spines.get("right", self.axes).get_window_extent()])
            self.label.set_position(
                (bbox.x1 + self.labelpad * self.get_figure(root=True).dpi / 72, y))
