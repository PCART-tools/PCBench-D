    def get_xminorticklabels(self):
        """
        Get the x minor tick labels

        Returns
        -------
        labels : list
            List of :class:`~matplotlib.text.Text` instances
        """
        return cbook.silent_list('Text xticklabel',
                                 self.xaxis.get_minorticklabels())
