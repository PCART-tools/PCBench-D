    def _long_axis(self):
        """Return the long axis"""
        if self.orientation == 'vertical':
            return self.ax.yaxis
        return self.ax.xaxis
