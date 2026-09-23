    def post_event(self):
        """
        Determines if it is a key event
        """
        if len(self.events) == 0:
            warnings.warn("No events yet")
        else:
            self.keyormouse = self.events[-1].name == 'key_press_event'
