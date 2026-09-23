    def get_size_inches(self):
        """
        Returns the current size of the figure in inches.

        Returns
        -------
        size : ndarray
           The size (width, height) of the figure in inches.

        See Also
        --------
        matplotlib.Figure.set_size_inches
        """
        return np.array(self.bbox_inches.p1)
