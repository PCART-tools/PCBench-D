    @property
    def axes(self):
        """
        Return a list with the row axis labels and column axis labels as the
        only members. They are returned in that order.
        """
        return [self.index, self.columns]
