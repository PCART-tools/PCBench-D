    def _message_cbk(self, event):
        """Capture the 'tool_message_event' and set the message."""
        self.set_message(event.message)
