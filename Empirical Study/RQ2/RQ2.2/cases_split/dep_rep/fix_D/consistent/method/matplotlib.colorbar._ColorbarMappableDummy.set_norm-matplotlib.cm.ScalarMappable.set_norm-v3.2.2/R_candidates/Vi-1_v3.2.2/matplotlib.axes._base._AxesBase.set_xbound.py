    def set_xbound(self, lower=None, upper=None):
        """
        Set the lower and upper numerical bounds of the x-axis.

        This method will honor axes inversion regardless of parameter order.
        It will not change the autoscaling setting (``Axes._autoscaleXon``).

        Parameters
        ----------
        lower, upper : float or None
            The lower and upper bounds. If *None*, the respective axis bound
            is not modified.

        See Also
        --------
        get_xbound
        get_xlim, set_xlim
        invert_xaxis, xaxis_inverted
        """
        if upper is None and np.iterable(lower):
            lower, upper = lower

        old_lower, old_upper = self.get_xbound()

        if lower is None:
            lower = old_lower
        if upper is None:
            upper = old_upper

        if self.xaxis_inverted():
            if lower < upper:
                self.set_xlim(upper, lower, auto=None)
            else:
                self.set_xlim(lower, upper, auto=None)
        else:
            if lower < upper:
                self.set_xlim(lower, upper, auto=None)
            else:
                self.set_xlim(upper, lower, auto=None)
