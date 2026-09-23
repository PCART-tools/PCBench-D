    def handle_unknown_event(self, event):
        _log.warning('Unhandled message type {0}. {1}'.format(
                     event['type'], event))
