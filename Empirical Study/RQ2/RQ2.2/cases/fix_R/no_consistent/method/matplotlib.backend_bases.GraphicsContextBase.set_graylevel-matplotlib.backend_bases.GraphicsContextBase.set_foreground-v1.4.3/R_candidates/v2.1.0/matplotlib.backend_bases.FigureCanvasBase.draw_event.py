    def draw_event(self, renderer):
        """Pass a `DrawEvent` to all functions connected to ``draw_event``."""
        s = 'draw_event'
        event = DrawEvent(s, self, renderer)
        self.callbacks.process(s, event)
