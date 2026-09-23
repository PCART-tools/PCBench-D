    def handle_event(self, event):
        e_type = event['type']
        handler = getattr(self, f'handle_{e_type}',
                          self.handle_unknown_event)
        return handler(event)
