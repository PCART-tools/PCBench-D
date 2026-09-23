    def get_size_inches(self):
        """
        Returns the current size of the figure in inches (1in == 2.54cm)
        as an numpy array.

        Returns
        -------
        size : ndarray
           The size of the figure in inches

        See Also
        --------

        matplotlib.Figure.set_size_inches
        """
        return np.array(self.bbox_inches.p1)
