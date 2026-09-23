class _AxesStack(cbook.Stack):
    """
    Specialization of Stack, to handle all tracking of Axes in a Figure.

    This stack stores ``ind, axes`` pairs, where ``ind`` is a serial index
    tracking the order in which axes were added.

    AxesStack is a callable; calling it returns the current axes.
    """

    def __init__(self):
        super().__init__()
        self._ind = 0

    def as_list(self):
        """
        Return a list of the Axes instances that have been added to the figure.
        """
        return [a for i, a in sorted(self._elements)]

    def _entry_from_axes(self, e):
        return next(((ind, a) for ind, a in self._elements if a == e), None)

    def remove(self, a):
        """Remove the axes from the stack."""
        super().remove(self._entry_from_axes(a))

    def bubble(self, a):
        """
        Move the given axes, which must already exist in the stack, to the top.
        """
        return super().bubble(self._entry_from_axes(a))

    def add(self, a):
        """
        Add Axes *a* to the stack.

        If *a* is already on the stack, don't add it again.
        """
        # All the error checking may be unnecessary; but this method
        # is called so seldom that the overhead is negligible.
        _api.check_isinstance(Axes, a=a)

        if a in self:
            return

        self._ind += 1
        super().push((self._ind, a))

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

    def __contains__(self, a):
        return a in self.as_list()
