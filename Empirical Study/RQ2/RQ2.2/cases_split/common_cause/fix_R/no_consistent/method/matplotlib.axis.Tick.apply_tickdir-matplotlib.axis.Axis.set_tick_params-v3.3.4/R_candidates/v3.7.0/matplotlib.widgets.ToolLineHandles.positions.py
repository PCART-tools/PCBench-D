    @property
    def positions(self):
        """Positions of the handle in data coordinates."""
        method = 'get_xdata' if self.direction == 'horizontal' else 'get_ydata'
        return [getattr(line, method)()[0] for line in self.artists]
