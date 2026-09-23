    def cleanup(self, event=None):
        """
        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`, optional
            Not used
        """
        # Clean the figure.
        if self.show_clicks:
            for mark in self.marks:
                mark.remove()
            self.marks = []
            self.fig.canvas.draw()
        # Call base class to remove callbacks.
        super().cleanup()
