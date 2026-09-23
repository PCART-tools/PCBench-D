    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred in the Tick marks.

        This function always returns false.  It is more useful to test if the
        axis as a whole contains the mouse rather than the set of tick marks.
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        return False, {}
