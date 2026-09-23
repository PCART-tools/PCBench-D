    def set_figure(self, fig):
        """
        Set the figure instance the artist belongs to.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
        """
        Text.set_figure(self, fig)
        self.dashline.set_figure(fig)
