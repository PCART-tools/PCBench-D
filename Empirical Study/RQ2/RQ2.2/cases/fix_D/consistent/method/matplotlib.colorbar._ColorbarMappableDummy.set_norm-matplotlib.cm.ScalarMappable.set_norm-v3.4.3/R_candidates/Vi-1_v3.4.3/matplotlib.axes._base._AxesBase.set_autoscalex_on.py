    def set_autoscalex_on(self, b):
        """
        Set whether autoscaling for the x-axis is applied to axes on the next
        draw or call to `.Axes.autoscale_view`.

        Parameters
        ----------
        b : bool
        """
        self._autoscaleXon = b
