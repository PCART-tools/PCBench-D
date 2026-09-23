    def sca(self, a):
        """Set the current axes to be *a* and return *a*."""
        self._axstack.bubble(a)
        self._axobservers.process("_axes_change_event", self)
        return a
