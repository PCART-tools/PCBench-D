    def _update_offset_text_position(self, bboxes, bboxes2):
        """
        Update the offset_text position based on the sequence of bounding
        boxes of all the ticklabels
        """
        x, y = self.offsetText.get_position()
        if not len(bboxes):
            bottom = self.axes.bbox.ymin
        else:
            bbox = mtransforms.Bbox.union(bboxes)
            bottom = bbox.y0
        self.offsetText.set_position(
            (x, bottom - self.OFFSETTEXTPAD * self.figure.dpi / 72)
        )
