    def get_xmajorticklabels(self):
        """
        Get the xtick major labels

        Returns
        -------
        labels : list
            List of :class:`~matplotlib.text.Text` instances
        """
        return cbook.silent_list('Text xticklabel',
                                 self.xaxis.get_majorticklabels())
