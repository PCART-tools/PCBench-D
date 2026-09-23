    def _get_data(self, event):
        """Get the xdata and ydata for event, with limits."""
        if event.xdata is None:
            return None, None
        xdata = np.clip(event.xdata, *self.ax.get_xbound())
        ydata = np.clip(event.ydata, *self.ax.get_ybound())
        return xdata, ydata
