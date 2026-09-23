    @property
    def handler(self):
        # for backward compatibility
        # web.Server instance
        return self.runner.server
