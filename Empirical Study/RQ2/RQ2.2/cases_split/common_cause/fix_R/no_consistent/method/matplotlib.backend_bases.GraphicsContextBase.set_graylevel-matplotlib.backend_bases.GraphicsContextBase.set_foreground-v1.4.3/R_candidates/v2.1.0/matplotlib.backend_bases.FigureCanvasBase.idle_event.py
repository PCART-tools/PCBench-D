    @cbook.deprecated("2.1")
    def idle_event(self, guiEvent=None):
        """Called when GUI is idle."""
        s = 'idle_event'
        event = IdleEvent(s, self, guiEvent=guiEvent)
        self.callbacks.process(s, event)
