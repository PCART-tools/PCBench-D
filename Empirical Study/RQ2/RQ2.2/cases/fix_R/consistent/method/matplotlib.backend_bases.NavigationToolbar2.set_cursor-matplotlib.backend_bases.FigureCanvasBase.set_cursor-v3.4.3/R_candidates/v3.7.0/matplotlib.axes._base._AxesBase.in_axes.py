    def in_axes(self, mouseevent):
        """
        Return whether the given event (in display coords) is in the Axes.
        """
        return self.patch.contains(mouseevent)[0]
