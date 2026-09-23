    def disconnect_events(self):
        """Disconnect all events created by this widget."""
        for c in self._cids:
            self.canvas.mpl_disconnect(c)
