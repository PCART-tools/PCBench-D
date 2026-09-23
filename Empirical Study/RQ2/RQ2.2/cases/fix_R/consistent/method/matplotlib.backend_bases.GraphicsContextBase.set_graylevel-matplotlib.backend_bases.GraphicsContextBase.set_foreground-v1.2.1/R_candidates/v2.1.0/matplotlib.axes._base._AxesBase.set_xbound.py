    def set_xbound(self, lower=None, upper=None):
        """
        Set the lower and upper numerical bounds of the x-axis.
        This method will honor axes inversion regardless of parameter order.
        It will not change the _autoscaleXon attribute.
        """
        if upper is None and iterable(lower):
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
