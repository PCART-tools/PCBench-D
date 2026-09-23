    def pick_event(self, mouseevent, artist, **kwargs):
        """
        This method will be called by artists who are picked and will
        fire off :class:`PickEvent` callbacks registered listeners
        """
        s = 'pick_event'
        event = PickEvent(s, self, mouseevent, artist,
                          guiEvent=mouseevent.guiEvent,
                          **kwargs)
        self.callbacks.process(s, event)
