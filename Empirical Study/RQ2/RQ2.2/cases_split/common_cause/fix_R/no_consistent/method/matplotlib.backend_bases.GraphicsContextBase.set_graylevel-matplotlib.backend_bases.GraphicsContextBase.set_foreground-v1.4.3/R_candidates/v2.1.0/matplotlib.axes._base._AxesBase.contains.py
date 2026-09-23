    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred in the axes.

        Returns *True* / *False*, {}
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)
        return self.patch.contains(mouseevent)
