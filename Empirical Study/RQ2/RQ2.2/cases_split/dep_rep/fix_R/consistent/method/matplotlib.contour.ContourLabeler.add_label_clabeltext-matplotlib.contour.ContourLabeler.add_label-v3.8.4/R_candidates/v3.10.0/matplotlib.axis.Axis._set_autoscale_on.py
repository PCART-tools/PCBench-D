    def _set_autoscale_on(self, b):
        """
        Set whether this Axis is autoscaled when drawing or by `.Axes.autoscale_view`.

        If b is None, then the value is not changed.

        Parameters
        ----------
        b : bool
        """
        if b is not None:
            self._autoscale_on = b
