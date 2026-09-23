    def set_ybound(self, lower=None, upper=None):
        """
        Set the lower and upper numerical bounds of the y-axis.

        This method will honor axes inversion regardless of parameter order.
        It will not change the autoscaling setting (``Axes._autoscaleYon``).

        Parameters
        ----------
        lower, upper : float or None
            The lower and upper bounds. If *None*, the respective axis bound
            is not modified.

        See Also
        --------
        get_ybound
        get_ylim, set_ylim
        invert_yaxis, yaxis_inverted
        """
        if upper is None and np.iterable(lower):
            lower, upper = lower

        old_lower, old_upper = self.get_ybound()

        if lower is None:
            lower = old_lower
        if upper is None:
            upper = old_upper

        if self.yaxis_inverted():
            if lower < upper:
                self.set_ylim(upper, lower, auto=None)
            else:
                self.set_ylim(lower, upper, auto=None)
        else:
            if lower < upper:
                self.set_ylim(lower, upper, auto=None)
            else:
                self.set_ylim(upper, lower, auto=None)
