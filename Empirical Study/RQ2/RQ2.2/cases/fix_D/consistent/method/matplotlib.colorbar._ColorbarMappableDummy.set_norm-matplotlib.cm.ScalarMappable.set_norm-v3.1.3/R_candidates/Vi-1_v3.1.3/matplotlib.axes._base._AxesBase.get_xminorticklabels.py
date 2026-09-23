    def get_xminorticklabels(self):
        """
        Get the minor x tick labels.

        Returns
        -------
        labels : list
            List of `~matplotlib.text.Text` instances
        """
        return cbook.silent_list('Text xticklabel',
                                 self.xaxis.get_minorticklabels())
