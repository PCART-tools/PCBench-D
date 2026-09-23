    @_api.deprecated("3.6")
    def get_ticklabel_extents(self, renderer):
        """Get the extents of the tick labels on either side of the axes."""
        ticks_to_draw = self._update_ticks()
        tlb1, tlb2 = self._get_ticklabel_bboxes(ticks_to_draw, renderer)
        if len(tlb1):
            bbox1 = mtransforms.Bbox.union(tlb1)
        else:
            bbox1 = mtransforms.Bbox.from_extents(0, 0, 0, 0)
        if len(tlb2):
            bbox2 = mtransforms.Bbox.union(tlb2)
        else:
            bbox2 = mtransforms.Bbox.from_extents(0, 0, 0, 0)
        return bbox1, bbox2
