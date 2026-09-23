    def _get_data(self, event):
        """Get the xdata and ydata for event, with limits."""
        if event.xdata is None:
            return None, None
        xdata, ydata = self._get_data_coords(event)
        xdata = np.clip(xdata, *self.ax.get_xbound())
        ydata = np.clip(ydata, *self.ax.get_ybound())
        return xdata, ydata
