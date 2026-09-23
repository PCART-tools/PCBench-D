    def _get_tick_boxes_siblings(self, renderer):
        """
        Get the bounding boxes for this `.axis` and its siblings
        as set by `.Figure.align_xlabels` or  `.Figure.align_ylabels`.

        By default, it just gets bboxes for *self*.
        """
        # Get the Grouper keeping track of x or y label groups for this figure.
        name = self._get_axis_name()
        if name not in self.figure._align_label_groups:
            return [], []
        grouper = self.figure._align_label_groups[name]
        bboxes = []
        bboxes2 = []
        # If we want to align labels from other Axes:
        for ax in grouper.get_siblings(self.axes):
            axis = ax._axis_map[name]
            ticks_to_draw = axis._update_ticks()
            tlb, tlb2 = axis._get_ticklabel_bboxes(ticks_to_draw, renderer)
            bboxes.extend(tlb)
            bboxes2.extend(tlb2)
        return bboxes, bboxes2
