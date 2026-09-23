    def _get_tick_boxes_siblings(self, renderer):
        """
        Get the bounding boxes for this `.axis` and its siblings
        as set by `.Figure.align_xlabels` or  `.Figure.align_ylablels`.

        By default it just gets bboxes for self.
        """
        bboxes = []
        bboxes2 = []
        # get the Grouper that keeps track of y-label groups for this figure
        grp = self.figure._align_ylabel_grp
        # if we want to align labels from other axes:
        for axx in grp.get_siblings(self.axes):
            ticks_to_draw = axx.yaxis._update_ticks()
            tlb, tlb2 = axx.yaxis._get_tick_bboxes(ticks_to_draw, renderer)
            bboxes.extend(tlb)
            bboxes2.extend(tlb2)
        return bboxes, bboxes2
