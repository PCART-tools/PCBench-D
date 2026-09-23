    def handle_event(self, event):
        e_type = event['type']
        handler = getattr(self, 'handle_{0}'.format(e_type),
                          self.handle_unknown_event)
        return handler(event)
