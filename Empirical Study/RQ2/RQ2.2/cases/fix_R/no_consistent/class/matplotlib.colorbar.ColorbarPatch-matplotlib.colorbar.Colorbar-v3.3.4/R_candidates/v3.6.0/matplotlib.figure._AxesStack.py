class _AxesStack:
    """
    Helper class to track axes in a figure.

    Axes are tracked both in the order in which they have been added
    (``self._axes`` insertion/iteration order) and in the separate "gca" stack
    (which is the index to which they map in the ``self._axes`` dict).
    """

    def __init__(self):
        self._axes = {}  # Mapping of axes to "gca" order.
        self._counter = itertools.count()

    def as_list(self):
        """List the axes that have been added to the figure."""
        return [*self._axes]  # This relies on dict preserving order.

    def remove(self, a):
        """Remove the axes from the stack."""
        self._axes.pop(a)

    def bubble(self, a):
        """Move an axes, which must already exist in the stack, to the top."""
        if a not in self._axes:
            raise ValueError("Axes has not been added yet")
        self._axes[a] = next(self._counter)

    def add(self, a):
        """Add an axes to the stack, ignoring it if already present."""
        if a not in self._axes:
            self._axes[a] = next(self._counter)

    def current(self):
        """Return the active axes, or None if the stack is empty."""
        return max(self._axes, key=self._axes.__getitem__, default=None)
