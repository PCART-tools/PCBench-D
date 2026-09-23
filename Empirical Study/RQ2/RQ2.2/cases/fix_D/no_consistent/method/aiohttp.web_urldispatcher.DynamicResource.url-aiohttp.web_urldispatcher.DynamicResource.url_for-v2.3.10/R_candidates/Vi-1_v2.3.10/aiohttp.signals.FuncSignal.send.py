    def send(self, *args, **kwargs):
        """
        Sends data to all registered receivers.
        """
        for receiver in self:
            receiver(*args, **kwargs)
