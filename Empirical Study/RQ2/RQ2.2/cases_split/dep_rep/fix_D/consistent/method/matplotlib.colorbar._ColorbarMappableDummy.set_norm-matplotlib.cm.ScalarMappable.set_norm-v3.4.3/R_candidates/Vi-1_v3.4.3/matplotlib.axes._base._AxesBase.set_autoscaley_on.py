    def set_autoscaley_on(self, b):
        """
        Set whether autoscaling for the y-axis is applied to axes on the next
        draw or call to `.Axes.autoscale_view`.

        Parameters
        ----------
        b : bool
        """
        self._autoscaleYon = b
