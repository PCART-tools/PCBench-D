    def get_data(self, orig=True):
        """
        Return the xdata, ydata.

        If *orig* is *True*, return the original data.
        """
        return self.get_xdata(orig=orig), self.get_ydata(orig=orig)
