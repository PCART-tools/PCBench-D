    @staticmethod
    def intersection(bbox1, bbox2):
        """
        Return the intersection of *bbox1* and *bbox2* if they intersect, or
        None if they don't.
        """
        x0 = np.maximum(bbox1.xmin, bbox2.xmin)
        x1 = np.minimum(bbox1.xmax, bbox2.xmax)
        y0 = np.maximum(bbox1.ymin, bbox2.ymin)
        y1 = np.minimum(bbox1.ymax, bbox2.ymax)
        return Bbox([[x0, y0], [x1, y1]]) if x0 <= x1 and y0 <= y1 else None
