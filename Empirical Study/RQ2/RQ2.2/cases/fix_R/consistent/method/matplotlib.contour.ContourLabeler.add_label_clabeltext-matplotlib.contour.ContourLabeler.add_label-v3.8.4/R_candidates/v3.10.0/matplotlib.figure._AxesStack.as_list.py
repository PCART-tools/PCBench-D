    def as_list(self):
        """List the Axes that have been added to the figure."""
        return [*self._axes]  # This relies on dict preserving order.
