    def bubble(self, a):
        """
        Move the given axes, which must already exist in the
        stack, to the top.
        """
        return super().bubble(self._entry_from_axes(a))
