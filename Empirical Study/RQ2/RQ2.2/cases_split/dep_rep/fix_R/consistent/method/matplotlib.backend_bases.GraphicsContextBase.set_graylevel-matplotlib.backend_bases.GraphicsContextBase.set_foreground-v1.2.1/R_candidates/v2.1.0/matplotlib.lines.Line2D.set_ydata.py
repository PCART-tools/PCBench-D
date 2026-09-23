    def set_ydata(self, y):
        """
        Set the data np.array for y

        ACCEPTS: 1D array
        """
        self._yorig = y
        self._invalidy = True
        self.stale = True
