    def setUp(self):
        self.loop = setup_test_loop()

        self.app = self.loop.run_until_complete(self.get_application())
        self.client = self.loop.run_until_complete(self._get_client(self.app))

        self.loop.run_until_complete(self.client.start_server())
