    def as_list(self):
        """
        Return a list of the Axes instances that have been added to the figure.
        """
        return [a for i, a in sorted(self._elements)]
