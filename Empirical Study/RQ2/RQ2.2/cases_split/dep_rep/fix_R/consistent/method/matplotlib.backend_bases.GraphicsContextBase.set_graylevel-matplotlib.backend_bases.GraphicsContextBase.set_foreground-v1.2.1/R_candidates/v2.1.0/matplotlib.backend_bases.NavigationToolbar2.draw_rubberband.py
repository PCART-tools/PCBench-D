    def draw_rubberband(self, event, x0, y0, x1, y1):
        """Draw a rectangle rubberband to indicate zoom limits.

        Note that it is not guaranteed that ``x0 <= x1`` and ``y0 <= y1``.
        """
