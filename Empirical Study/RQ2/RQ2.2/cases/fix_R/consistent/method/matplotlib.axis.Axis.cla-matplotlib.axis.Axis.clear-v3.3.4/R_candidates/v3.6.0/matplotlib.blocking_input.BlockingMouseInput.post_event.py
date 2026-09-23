    def post_event(self):
        """Process an event."""
        if len(self.events) == 0:
            _log.warning("No events yet")
        elif self.events[-1].name == 'key_press_event':
            self.key_event()
        else:
            self.mouse_event()
