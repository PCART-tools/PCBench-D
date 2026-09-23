    def mouse_event_add(self, event):
        """
        Will be called for any event involving a button other than
        button 2 or 3.  This will add a click if it is inside axes.
        """
        if event.inaxes:
            self.add_click(event)
        else:  # If not a valid click, remove from event list
            BlockingInput.pop(self, -1)
