    def get_xmajorticklabels(self):
        """
        Get the major x tick labels.

        Returns
        -------
        labels : list
            List of `~matplotlib.text.Text` instances
        """
        return self.xaxis.get_majorticklabels()
