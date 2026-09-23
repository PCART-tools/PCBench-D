    def _send_event(self, event_type, **kwargs):
        payload = {'type': event_type, **kwargs}
        for s in self.web_sockets:
            s.send_json(payload)
