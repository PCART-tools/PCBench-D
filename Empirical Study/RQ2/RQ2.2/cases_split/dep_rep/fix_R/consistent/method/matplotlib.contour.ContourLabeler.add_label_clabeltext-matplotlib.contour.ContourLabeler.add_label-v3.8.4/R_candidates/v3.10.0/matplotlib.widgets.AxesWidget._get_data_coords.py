    def _get_data_coords(self, event):
        """Return *event*'s data coordinates in this widget's Axes."""
        # This method handles the possibility that event.inaxes != self.ax (which may
        # occur if multiple Axes are overlaid), in which case event.xdata/.ydata will
        # be wrong.  Note that we still special-case the common case where
        # event.inaxes == self.ax and avoid re-running the inverse data transform,
        # because that can introduce floating point errors for synthetic events.
        return ((event.xdata, event.ydata) if event.inaxes is self.ax
                else self.ax.transData.inverted().transform((event.x, event.y)))
