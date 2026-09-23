    def _pre_setup(self):
        """
        Perform pre-test setup:
        * Create a test client.
        * Clear the mail test outbox.
        """
        self.client = self.client_class()
        self.async_client = self.async_client_class()
        mail.outbox = []
