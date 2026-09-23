    def handle_unknown_event(self, event):
        warnings.warn('Unhandled message type {0}. {1}'.format(
            event['type'], event), stacklevel=2)
