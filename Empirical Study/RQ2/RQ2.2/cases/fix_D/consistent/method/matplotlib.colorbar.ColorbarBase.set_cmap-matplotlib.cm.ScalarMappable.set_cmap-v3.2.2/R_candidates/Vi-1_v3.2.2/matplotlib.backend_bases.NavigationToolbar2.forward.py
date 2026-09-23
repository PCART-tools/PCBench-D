    def forward(self, *args):
        """Move forward in the view lim stack."""
        self._nav_stack.forward()
        self.set_history_buttons()
        self._update_view()
