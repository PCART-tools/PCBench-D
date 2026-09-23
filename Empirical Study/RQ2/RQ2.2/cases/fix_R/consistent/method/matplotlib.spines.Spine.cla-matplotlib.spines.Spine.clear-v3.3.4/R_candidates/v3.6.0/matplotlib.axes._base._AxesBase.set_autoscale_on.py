    def set_autoscale_on(self, b):
        """
        Set whether autoscaling is applied to each axis on the next draw or
        call to `.Axes.autoscale_view`.

        Parameters
        ----------
        b : bool
        """
        for axis in self._axis_map.values():
            axis._set_autoscale_on(b)
