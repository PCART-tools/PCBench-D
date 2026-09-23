    def _update_label_position(self, bboxes, bboxes2):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        if not self._autolabelpos:
            return
        x, y = self.label.get_position()
        if self.label_position == 'bottom':
            try:
                spine = self.axes.spines['bottom']
                spinebbox = spine.get_transform().transform_path(
                    spine.get_path()).get_extents()
            except KeyError:
                # use axes if spine doesn't exist
                spinebbox = self.axes.bbox
            bbox = mtransforms.Bbox.union(bboxes + [spinebbox])
            bottom = bbox.y0

            self.label.set_position(
                (x, bottom - self.labelpad * self.figure.dpi / 72.0)
            )

        else:
            try:
                spine = self.axes.spines['top']
                spinebbox = spine.get_transform().transform_path(
                    spine.get_path()).get_extents()
            except KeyError:
                # use axes if spine doesn't exist
                spinebbox = self.axes.bbox
            bbox = mtransforms.Bbox.union(bboxes2 + [spinebbox])
            top = bbox.y1

            self.label.set_position(
                (x, top + self.labelpad * self.figure.dpi / 72.0)
            )
