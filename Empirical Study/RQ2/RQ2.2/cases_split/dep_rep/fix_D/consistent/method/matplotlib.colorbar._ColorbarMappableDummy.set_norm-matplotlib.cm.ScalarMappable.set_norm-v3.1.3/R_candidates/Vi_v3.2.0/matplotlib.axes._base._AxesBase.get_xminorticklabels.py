    def get_xminorticklabels(self):
        """
        Get the minor x tick labels.

        Returns
        -------
        labels : list
            List of `~matplotlib.text.Text` instances
        """
        return self.xaxis.get_minorticklabels()
