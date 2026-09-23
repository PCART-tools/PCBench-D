    @staticmethod
    def union(bboxes):
        """
        Return a :class:`Bbox` that contains all of the given bboxes.
        """
        if not len(bboxes):
            raise ValueError("'bboxes' cannot be empty")
        x0 = np.min([bbox.xmin for bbox in bboxes])
        x1 = np.max([bbox.xmax for bbox in bboxes])
        y0 = np.min([bbox.ymin for bbox in bboxes])
        y1 = np.max([bbox.ymax for bbox in bboxes])
        return Bbox([[x0, y0], [x1, y1]])
