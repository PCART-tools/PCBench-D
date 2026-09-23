    def __call__(self):
        """
        Return the active axes.

        If no axes exists on the stack, then returns None.
        """
        if not len(self._elements):
            return None
        else:
            index, axes = self._elements[self._pos]
            return axes
