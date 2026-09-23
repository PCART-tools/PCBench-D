    def set_data(self, *args):
        """
        Set the x and y data

        ACCEPTS: 2D array (rows are x, y) or two 1D arrays
        """
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args

        self.set_xdata(x)
        self.set_ydata(y)
