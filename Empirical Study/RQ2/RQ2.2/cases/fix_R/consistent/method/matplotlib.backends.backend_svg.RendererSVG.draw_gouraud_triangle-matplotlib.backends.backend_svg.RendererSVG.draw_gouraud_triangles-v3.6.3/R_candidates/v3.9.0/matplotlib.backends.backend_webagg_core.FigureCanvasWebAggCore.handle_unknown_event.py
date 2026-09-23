    def handle_unknown_event(self, event):
        _log.warning('Unhandled message type %s. %s', event["type"], event)
