    def get_ymajorticklabels(self):
        """
        Get the major y tick labels.

        Returns
        -------
        labels : list
            List of `~matplotlib.text.Text` instances
        """
        return self.yaxis.get_majorticklabels()
