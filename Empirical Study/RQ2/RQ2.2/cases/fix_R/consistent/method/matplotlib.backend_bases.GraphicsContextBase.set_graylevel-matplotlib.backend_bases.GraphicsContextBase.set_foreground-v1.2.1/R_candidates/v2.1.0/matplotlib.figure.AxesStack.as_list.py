    def as_list(self):
        """
        Return a list of the Axes instances that have been added to the figure
        """
        ia_list = [a for k, a in self._elements]
        ia_list.sort()
        return [a for i, a in ia_list]
