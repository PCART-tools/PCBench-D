    def trigger(self, *args, **kwargs):
        message = "Copy tool is not available"
        self.toolmanager.message_event(message, self)
