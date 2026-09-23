    def setUp(self):
        self.loop = setup_test_loop()
        self.app = self.get_app(self.loop)
        self.client = TestClient(self.app)
        self.loop.run_until_complete(self.client.start_server())
