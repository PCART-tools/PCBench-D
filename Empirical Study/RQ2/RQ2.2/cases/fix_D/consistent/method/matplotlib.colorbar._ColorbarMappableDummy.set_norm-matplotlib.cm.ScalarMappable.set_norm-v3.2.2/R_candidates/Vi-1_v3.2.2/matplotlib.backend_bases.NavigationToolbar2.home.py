    def home(self, *args):
        """Restore the original view."""
        self._nav_stack.home()
        self.set_history_buttons()
        self._update_view()
