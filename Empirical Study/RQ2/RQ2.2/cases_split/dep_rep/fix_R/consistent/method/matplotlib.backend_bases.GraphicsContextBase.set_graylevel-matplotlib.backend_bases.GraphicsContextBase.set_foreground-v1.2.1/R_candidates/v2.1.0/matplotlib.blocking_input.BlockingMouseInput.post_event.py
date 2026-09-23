    def post_event(self):
        """
        This will be called to process events
        """
        if len(self.events) == 0:
            warnings.warn("No events yet")
        elif self.events[-1].name == 'key_press_event':
            self.key_event()
        else:
            self.mouse_event()
