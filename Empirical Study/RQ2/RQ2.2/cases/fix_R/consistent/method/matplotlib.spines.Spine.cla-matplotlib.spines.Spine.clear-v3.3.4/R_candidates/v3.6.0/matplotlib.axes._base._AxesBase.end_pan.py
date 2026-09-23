    def end_pan(self):
        """
        Called when a pan operation completes (when the mouse button is up.)

        Notes
        -----
        This is intended to be overridden by new projection types.
        """
        del self._pan_start
