    def count_overlaps(self, bboxes):
        """
        Count the number of bounding boxes that overlap this one.

        bboxes is a sequence of :class:`BboxBase` objects
        """
        return count_bboxes_overlapping_bbox(
            self, np.atleast_3d([np.array(x) for x in bboxes]))
