    def get_xbound(self):
        """
        Return the lower and upper x-axis bounds, in increasing order.

        See Also
        --------
        set_xbound
        get_xlim, set_xlim
        invert_xaxis, xaxis_inverted
        """
        left, right = self.get_xlim()
        if left < right:
            return left, right
        else:
            return right, left
