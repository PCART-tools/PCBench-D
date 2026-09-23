    def get_ybound(self):
        """
        Return y-axis numerical bounds in the form of
        ``lowerBound < upperBound``
        """
        bottom, top = self.get_ylim()
        if bottom < top:
            return bottom, top
        else:
            return top, bottom
