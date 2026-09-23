    def get_yminorticklabels(self):
        """
        Get the minor y tick labels.

        Returns
        -------
        labels : list
            List of `~matplotlib.text.Text` instances
        """
        return self.yaxis.get_minorticklabels()
