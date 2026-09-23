    def get_yminorticklabels(self):
        """
        Get the minor y tick labels

        Returns
        -------
        labels : list
            List of :class:`~matplotlib.text.Text` instances
        """
        return cbook.silent_list('Text yticklabel',
                                 self.yaxis.get_minorticklabels())
