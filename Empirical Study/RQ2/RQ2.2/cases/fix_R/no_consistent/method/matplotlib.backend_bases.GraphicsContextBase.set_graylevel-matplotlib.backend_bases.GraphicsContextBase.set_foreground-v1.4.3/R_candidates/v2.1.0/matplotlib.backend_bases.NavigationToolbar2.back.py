    def back(self, *args):
        """move back up the view lim stack"""
        self._views.back()
        self._positions.back()
        self.set_history_buttons()
        self._update_view()
