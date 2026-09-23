    def _on_units_changed(self, scalex=False, scaley=False):
        """
        Callback for processing changes to axis units.

        Currently requests updates of data limits and view limits.
        """
        self.relim()
        self._request_autoscale_view(scalex=scalex, scaley=scaley)
