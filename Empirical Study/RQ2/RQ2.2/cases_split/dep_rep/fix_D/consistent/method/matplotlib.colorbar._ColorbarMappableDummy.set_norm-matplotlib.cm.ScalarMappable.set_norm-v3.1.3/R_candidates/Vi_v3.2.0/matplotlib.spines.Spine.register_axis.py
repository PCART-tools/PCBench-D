    def register_axis(self, axis):
        """Register an axis.

        An axis should be registered with its corresponding spine from
        the Axes instance. This allows the spine to clear any axis
        properties when needed.
        """
        self.axis = axis
        if self.axis is not None:
            self.axis.cla()
        self.stale = True
