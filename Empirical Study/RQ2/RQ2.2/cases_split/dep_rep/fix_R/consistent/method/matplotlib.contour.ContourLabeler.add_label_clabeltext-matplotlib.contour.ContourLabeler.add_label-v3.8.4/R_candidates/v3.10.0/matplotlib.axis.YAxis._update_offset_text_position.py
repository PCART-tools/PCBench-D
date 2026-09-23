    def _update_offset_text_position(self, bboxes, bboxes2):
        """
        Update the offset_text position based on the sequence of bounding
        boxes of all the ticklabels
        """
        x, _ = self.offsetText.get_position()
        if 'outline' in self.axes.spines:
            # Special case for colorbars:
            bbox = self.axes.spines['outline'].get_window_extent()
        else:
            bbox = self.axes.bbox
        top = bbox.ymax
        self.offsetText.set_position(
            (x, top + self.OFFSETTEXTPAD * self.get_figure(root=True).dpi / 72)
        )
