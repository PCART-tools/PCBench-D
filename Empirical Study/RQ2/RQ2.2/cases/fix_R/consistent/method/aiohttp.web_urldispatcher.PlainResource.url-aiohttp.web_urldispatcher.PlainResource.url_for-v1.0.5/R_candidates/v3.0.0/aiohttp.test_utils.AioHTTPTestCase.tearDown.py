    def tearDown(self):
        self.loop.run_until_complete(self.tearDownAsync())
        self.loop.run_until_complete(self.client.close())
        teardown_test_loop(self.loop)
