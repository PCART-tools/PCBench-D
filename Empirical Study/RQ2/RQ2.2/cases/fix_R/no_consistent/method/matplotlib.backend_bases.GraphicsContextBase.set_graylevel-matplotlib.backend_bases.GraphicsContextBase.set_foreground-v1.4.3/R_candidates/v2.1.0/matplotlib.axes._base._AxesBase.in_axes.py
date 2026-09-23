    def in_axes(self, mouseevent):
        """
        Return *True* if the given *mouseevent* (in display coords)
        is in the Axes
        """
        return self.patch.contains(mouseevent)[0]
