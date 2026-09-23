    def home(self, *args):
        """Restore the original view."""
        self._views.home()
        self._positions.home()
        self.set_history_buttons()
        self._update_view()
