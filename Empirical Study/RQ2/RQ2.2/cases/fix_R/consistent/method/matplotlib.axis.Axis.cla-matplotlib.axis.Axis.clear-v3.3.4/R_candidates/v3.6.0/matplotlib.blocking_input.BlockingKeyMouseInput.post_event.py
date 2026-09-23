    def post_event(self):
        """Determine if it is a key event."""
        if self.events:
            self.keyormouse = self.events[-1].name == 'key_press_event'
        else:
            _log.warning("No events yet.")
