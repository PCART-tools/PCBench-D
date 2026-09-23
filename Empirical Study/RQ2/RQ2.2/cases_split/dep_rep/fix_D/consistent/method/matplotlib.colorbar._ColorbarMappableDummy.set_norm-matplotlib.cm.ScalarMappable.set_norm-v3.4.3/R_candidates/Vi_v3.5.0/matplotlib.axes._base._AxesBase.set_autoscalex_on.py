    def set_autoscalex_on(self, b):
        """
        Set whether the x-axis is autoscaled on the next draw or call to
        `.Axes.autoscale_view`.

        Parameters
        ----------
        b : bool
        """
        self._autoscaleXon = b
