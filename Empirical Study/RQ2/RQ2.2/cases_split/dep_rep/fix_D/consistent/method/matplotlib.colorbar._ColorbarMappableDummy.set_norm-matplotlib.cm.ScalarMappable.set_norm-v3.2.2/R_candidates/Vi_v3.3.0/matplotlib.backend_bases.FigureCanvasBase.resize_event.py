    def resize_event(self):
        """
        Pass a `ResizeEvent` to all functions connected to ``resize_event``.
        """
        s = 'resize_event'
        event = ResizeEvent(s, self)
        self.callbacks.process(s, event)
        self.draw_idle()
