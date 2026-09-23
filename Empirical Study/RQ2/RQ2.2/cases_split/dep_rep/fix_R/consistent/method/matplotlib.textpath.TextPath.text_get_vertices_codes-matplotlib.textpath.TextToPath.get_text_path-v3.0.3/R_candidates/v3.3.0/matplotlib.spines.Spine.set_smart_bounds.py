    @cbook.deprecated("3.2")
    def set_smart_bounds(self, value):
        """Set the spine and associated axis to have smart bounds."""
        self._smart_bounds = value

        # also set the axis if possible
        if self.spine_type in ('left', 'right'):
            self.axes.yaxis.set_smart_bounds(value)
        elif self.spine_type in ('top', 'bottom'):
            self.axes.xaxis.set_smart_bounds(value)
        self.stale = True
