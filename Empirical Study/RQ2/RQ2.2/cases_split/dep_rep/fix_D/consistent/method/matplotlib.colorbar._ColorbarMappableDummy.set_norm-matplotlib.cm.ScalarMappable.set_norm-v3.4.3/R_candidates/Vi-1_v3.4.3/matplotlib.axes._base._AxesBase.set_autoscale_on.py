    def set_autoscale_on(self, b):
        """
        Set whether autoscaling is applied to axes on the next draw or call to
        `.Axes.autoscale_view`.

        Parameters
        ----------
        b : bool
        """
        self._autoscaleXon = b
        self._autoscaleYon = b
