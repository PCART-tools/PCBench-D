    def _changed_canvas(self):
        """
        Someone has switched the canvas on us!

        This happens if `savefig` needs to save to a format the previous
        backend did not support (e.g. saving a figure using an Agg based
        backend saved to a vector format).

        Returns
        -------
        bool
           True if the canvas has been changed.

        """
        return self.canvas is not self.ax.figure.canvas
