    def setUp(self):
        self.loop = setup_test_loop()

        self.app = self.loop.run_until_complete(self.get_application())
        self.server = self.loop.run_until_complete(self.get_server(self.app))
        self.client = self.loop.run_until_complete(
            self.get_client(self.server))

        self.loop.run_until_complete(self.client.start_server())

        self.loop.run_until_complete(self.setUpAsync())
