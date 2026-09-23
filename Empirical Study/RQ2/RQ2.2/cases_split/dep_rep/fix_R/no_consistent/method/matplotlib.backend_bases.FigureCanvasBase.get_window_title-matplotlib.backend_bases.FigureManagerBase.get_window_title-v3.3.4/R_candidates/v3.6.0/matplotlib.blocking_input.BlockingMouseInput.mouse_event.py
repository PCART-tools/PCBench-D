    def mouse_event(self):
        """Process a mouse click event."""
        event = self.events[-1]
        button = event.button
        if button == self.button_pop:
            self.mouse_event_pop(event)
        elif button == self.button_stop:
            self.mouse_event_stop(event)
        elif button == self.button_add:
            self.mouse_event_add(event)
