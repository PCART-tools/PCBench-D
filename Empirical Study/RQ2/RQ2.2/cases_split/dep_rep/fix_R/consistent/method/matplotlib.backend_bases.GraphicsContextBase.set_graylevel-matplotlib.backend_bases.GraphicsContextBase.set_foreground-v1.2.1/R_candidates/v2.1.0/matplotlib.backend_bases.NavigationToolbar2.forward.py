    def forward(self, *args):
        """Move forward in the view lim stack."""
        self._views.forward()
        self._positions.forward()
        self.set_history_buttons()
        self._update_view()
