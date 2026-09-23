    def _on_timer(self):
        TimerBase._on_timer(self)

        # Gtk timeout_add() requires that the callback returns True if it
        # is to be called again.
        if len(self.callbacks) > 0 and not self._single:
            return True
        else:
            self._timer = None
            return False
