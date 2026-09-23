    def get_ybound(self):
        """
        Return the lower and upper y-axis bounds, in increasing order.

        See Also
        --------
        set_ybound
        get_ylim, set_ylim
        invert_yaxis, yaxis_inverted
        """
        bottom, top = self.get_ylim()
        if bottom < top:
            return bottom, top
        else:
            return top, bottom
