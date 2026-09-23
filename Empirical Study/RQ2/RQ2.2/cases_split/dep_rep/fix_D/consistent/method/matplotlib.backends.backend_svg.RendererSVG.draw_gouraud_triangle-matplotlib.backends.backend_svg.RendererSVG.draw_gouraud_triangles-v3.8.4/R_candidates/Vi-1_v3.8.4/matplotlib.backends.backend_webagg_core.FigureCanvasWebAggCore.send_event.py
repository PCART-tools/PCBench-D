    def send_event(self, event_type, **kwargs):
        if self.manager:
            self.manager._send_event(event_type, **kwargs)
