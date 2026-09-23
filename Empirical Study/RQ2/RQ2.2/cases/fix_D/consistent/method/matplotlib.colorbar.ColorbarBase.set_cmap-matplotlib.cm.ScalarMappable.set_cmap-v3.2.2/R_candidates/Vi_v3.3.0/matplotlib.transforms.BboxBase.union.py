    @staticmethod
    def union(bboxes):
        """Return a `Bbox` that contains all of the given *bboxes*."""
        if not len(bboxes):
            raise ValueError("'bboxes' cannot be empty")
        # needed for 1.14.4 < numpy_version < 1.16
        # can remove once we are at numpy >= 1.16
        with np.errstate(invalid='ignore'):
            x0 = np.min([bbox.xmin for bbox in bboxes])
            x1 = np.max([bbox.xmax for bbox in bboxes])
            y0 = np.min([bbox.ymin for bbox in bboxes])
            y1 = np.max([bbox.ymax for bbox in bboxes])
        return Bbox([[x0, y0], [x1, y1]])
