    @property
    def connectors(self):
        """
        4-tuple of `.patches.ConnectionPatch` or None
            The four connector lines connecting to (lower_left, upper_left,
            lower_right upper_right) corners of *inset_ax*. Two lines are
            set with visibility to *False*,  but the user can set the
            visibility to True if the automatic choice is not deemed correct.
        """
        if self._inset_ax is None:
            return

        if self._auto_update_bounds:
            self._rectangle.set_bounds(self._bounds_from_inset_ax())
        self._update_connectors()
        return tuple(self._connectors)
