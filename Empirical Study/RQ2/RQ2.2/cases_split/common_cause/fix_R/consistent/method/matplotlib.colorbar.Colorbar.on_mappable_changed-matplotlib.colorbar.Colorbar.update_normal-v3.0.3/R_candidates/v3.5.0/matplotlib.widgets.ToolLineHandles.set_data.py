    def set_data(self, positions):
        """
        Set x or y positions of handles, depending if the lines are vertical
        of horizontal.

        Parameters
        ----------
        positions : tuple of length 2
            Set the positions of the handle in data coordinates
        """
        method = 'set_xdata' if self.direction == 'horizontal' else 'set_ydata'
        for line, p in zip(self.artists, positions):
            getattr(line, method)([p, p])
