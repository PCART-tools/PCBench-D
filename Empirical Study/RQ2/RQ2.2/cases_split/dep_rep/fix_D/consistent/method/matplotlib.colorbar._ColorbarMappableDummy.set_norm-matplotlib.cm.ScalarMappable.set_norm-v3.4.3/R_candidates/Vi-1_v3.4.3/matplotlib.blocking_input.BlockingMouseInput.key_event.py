    def key_event(self):
        """
        Process a key press event, mapping keys to appropriate mouse clicks.
        """
        event = self.events[-1]
        if event.key is None:
            # At least in OSX gtk backend some keys return None.
            return
        if event.key in ['backspace', 'delete']:
            self.mouse_event_pop(event)
        elif event.key in ['escape', 'enter']:
            self.mouse_event_stop(event)
        else:
            self.mouse_event_add(event)
