    def get_ybound(self):
        """Return the lower and upper y-axis bounds, in increasing order."""
        bottom, top = self.get_ylim()
        if bottom < top:
            return bottom, top
        else:
            return top, bottom
