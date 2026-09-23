    def set_autoscaley_on(self, b):
        """
        Set whether the y-axis is autoscaled on the next draw or call to
        `.Axes.autoscale_view`.

        Parameters
        ----------
        b : bool
        """
        self._autoscaleYon = b
