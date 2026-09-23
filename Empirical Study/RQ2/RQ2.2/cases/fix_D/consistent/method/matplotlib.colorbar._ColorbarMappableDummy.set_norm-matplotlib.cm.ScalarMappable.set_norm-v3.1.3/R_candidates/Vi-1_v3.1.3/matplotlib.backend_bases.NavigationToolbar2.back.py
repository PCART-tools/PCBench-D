    def back(self, *args):
        """move back up the view lim stack"""
        self._nav_stack.back()
        self.set_history_buttons()
        self._update_view()
