    def close_event(self, guiEvent=None):
        """Pass a `CloseEvent` to all functions connected to ``close_event``.
        """
        s = 'close_event'
        try:
            event = CloseEvent(s, self, guiEvent=guiEvent)
            self.callbacks.process(s, event)
        except (TypeError, AttributeError):
            pass
