    def set_xbound(self, lower=None, upper=None):
        """
        Set the lower and upper numerical bounds of the x-axis.

        This method will honor axis inversion regardless of parameter order.
        It will not change the autoscaling setting (`.get_autoscalex_on()`).

        Parameters
        ----------
        lower, upper : float or None
            The lower and upper bounds. If *None*, the respective axis bound
            is not modified.

            .. ACCEPTS: (lower: float, upper: float)

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

        self.set_xlim(sorted((lower, upper),
                             reverse=bool(self.xaxis_inverted())),
                      auto=None)
