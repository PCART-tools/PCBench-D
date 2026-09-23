    def get_ymajorticklabels(self):
        """
        Get the major y tick labels.

        Returns
        -------
        labels : list
            List of :class:`~matplotlib.text.Text` instances
        """
        return cbook.silent_list('Text yticklabel',
                                 self.yaxis.get_majorticklabels())
