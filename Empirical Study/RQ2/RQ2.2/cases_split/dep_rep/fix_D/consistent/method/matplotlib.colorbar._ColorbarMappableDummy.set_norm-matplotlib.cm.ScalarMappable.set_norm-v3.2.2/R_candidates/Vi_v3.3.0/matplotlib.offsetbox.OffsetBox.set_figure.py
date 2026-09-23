    def set_figure(self, fig):
        """
        Set the `.Figure` for the `.OffsetBox` and all its children.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
        """
        martist.Artist.set_figure(self, fig)
        for c in self.get_children():
            c.set_figure(fig)
