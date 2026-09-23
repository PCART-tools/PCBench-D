    def send_event(self, event_type, **kwargs):
        self.manager._send_event(event_type, **kwargs)
