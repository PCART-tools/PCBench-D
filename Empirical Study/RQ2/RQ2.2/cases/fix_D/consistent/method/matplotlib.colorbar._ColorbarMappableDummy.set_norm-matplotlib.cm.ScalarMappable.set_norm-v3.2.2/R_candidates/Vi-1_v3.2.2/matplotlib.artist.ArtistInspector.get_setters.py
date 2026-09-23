    def get_setters(self):
        """
        Get the attribute strings with setters for object.  e.g., for a line,
        return ``['markerfacecolor', 'linewidth', ....]``.
        """
        return [prop for prop, target in self._get_setters_and_targets()]
