    def _update_offset_text_position(self, bboxes, bboxes2):
        """
        Update the offset_text position based on the sequence of bounding
        boxes of all the ticklabels
        """
        x, y = self.offsetText.get_position()
        if not hasattr(self, '_tick_position'):
            self._tick_position = 'bottom'
        if self._tick_position == 'bottom':
            if not len(bboxes):
                bottom = self.axes.bbox.ymin
            else:
                bbox = mtransforms.Bbox.union(bboxes)
                bottom = bbox.y0
            y = bottom - self.OFFSETTEXTPAD * self.figure.dpi / 72
        else:
            if not len(bboxes2):
                top = self.axes.bbox.ymax
            else:
                bbox = mtransforms.Bbox.union(bboxes2)
                top = bbox.y1
            y = top + self.OFFSETTEXTPAD * self.figure.dpi / 72
        self.offsetText.set_position((x, y))
