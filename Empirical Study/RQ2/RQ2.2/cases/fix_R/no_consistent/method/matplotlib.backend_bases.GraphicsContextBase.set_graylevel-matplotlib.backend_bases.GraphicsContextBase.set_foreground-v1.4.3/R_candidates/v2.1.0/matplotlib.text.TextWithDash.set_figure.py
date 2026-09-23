    def set_figure(self, fig):
        """
        Set the figure instance the artist belong to.

        ACCEPTS: a :class:`matplotlib.figure.Figure` instance
        """
        Text.set_figure(self, fig)
        self.dashline.set_figure(fig)
