    def overlaps(self, other):
        """
        Return whether this bounding box overlaps with the other bounding box.

        Parameters
        ----------
        other : BboxBase
        """
        ax1, ay1, ax2, ay2 = self.extents
        bx1, by1, bx2, by2 = other.extents
        if ax2 < ax1:
            ax2, ax1 = ax1, ax2
        if ay2 < ay1:
            ay2, ay1 = ay1, ay2
        if bx2 < bx1:
            bx2, bx1 = bx1, bx2
        if by2 < by1:
            by2, by1 = by1, by2
        return ax1 <= bx2 and bx1 <= ax2 and ay1 <= by2 and by1 <= ay2
